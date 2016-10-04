var DjangoLinkDialog = ( function( $ ) {
    'use strict';

    CKEDITOR.dialog.add('djangolink', function( editor ) {
        var anchors;
        var plugin = CKEDITOR.plugins.djangolink;
        var linkplugin = CKEDITOR.plugins.link;
        var commonLang = editor.lang.common;
        var linkLang = editor.lang.link;
        var dialog = {
            title: 'Link',
            minWidth: 800,
            minHeight: 400,
            contents: [ {
                elements: [ {
                    type: 'html',
                    html: '<iframe style="position:static; width:100%; height:100%; border:none;" />'
                } ]
            } ],
            onOk: on_ok,
            onShow: on_show
        };

        function on_ok() {
            console.log('on ok')

            var data = {};
            var verify_url = editor.config.djangolinkVerifyURL;
            var $iframe = $( CKEDITOR.dialog.getCurrent().parts.contents.$ ).find('iframe').contents();
            var $form = $iframe.find('form');
            var $fields = $form.find("input, select");

            for ( var i = 0; i < $fields.length; i++ ) {
                data[ $fields[ i ].name ] = $fields[ i ].value;
            }

            $.ajax( {
                'url': verify_url,
                'method':
                'post',
                'data': data,
                //'success': ajax_success,
            } ).then( $.proxy( ajax_success, this ) );

            function ajax_success( response_data, xhr ) {
                // on django form error
                if ( response_data.valid != 'true') {
                    show_form_errors( $form, response_data );
                    return false;
                }

                var selection = editor.getSelection();
                var attributes = plugin.getLinkAttributes(
                    editor,
                    response_data.data,
                    response_data.link_value
                );
                console.log(selection)
                console.log(this._.selectedElement)
                if ( !this._.selectedElement ) {
                    var range = selection.getRanges()[ 0 ];

                    // TODO: there is "link" as link text if none
                    if ( range.collapsed ) {
                        var text = new CKEDITOR.dom.text('link', editor.document );
                        range.insertNode(text);
                        range.selectNodeContents(text);
                    }

                    // Apply style.
                    var style = new CKEDITOR.style( {
                        element: 'a',
                        attributes: attributes.set
                    } );

                    style.type = CKEDITOR.STYLE_INLINE; // need to override... dunno why.
                    style.applyToRange( range, editor );
                    range.select();
                } else {
                    // We're only editing an existing link, so just overwrite the attributes.
                    var element = this._.selectedElement;
                    var href = element.data( 'cke-saved-href' );
                    var textView = element.getHtml();

                    element.setAttributes( attributes.set );
                    element.removeAttributes( attributes.removed );

                    // Update text view when user changes protocol (#4612).
                    if ( href == textView || data.type == 'email' && textView.indexOf( '@' ) != -1 ) {
                        // Short mailto link text view (#5736).
                        element.setHtml( data.type == 'email' ?
                            data.email.address : attributes.set[ 'data-cke-saved-href' ] );

                        // We changed the content, so need to select it again.
                        selection.selectElement( element );
                    }

                    delete this._.selectedElement;

                }
                CKEDITOR.dialog.getCurrent().hide();
                // TODO: better remove/refresh iframe??
                $iframe.attr("src", "");
            };

            return false;
        };

        function show_form_errors( $form, data ) {
            // clean old errors
            $('.form-rows', $form).removeClass("errors");
            $('.errorlist', $form).remove();
            // attach new errors
            for ( var i = 0; i < data.errors.length; i++ ) {
                var name = data.errors[ i ].shift();
                var $field = $('.form-row.field-' + name, $form);
                var html = '<ul class="errorlist">';
                for ( var e = 0; e <  data.errors[ i ].length; e++ ) {
                    html += '<li>' +  data.errors[ i ][ e ] + '</li>';
                }
                html += '</ul>';
                $field.addClass("errors");
                $field.prepend( html );
            }
        };

        function on_show() {
            console.log('on show')
            var editor = this.getParentEditor(),
                selection = editor.getSelection(),
                element = null;

            // Fill in all the relevant fields if there's already one link selected.
            if ( ( element = plugin.getSelectedLink( editor ) ) && element.hasAttribute( 'href' ) ) {
                // Don't change selection if some element is already selected.
                // For example - don't destroy fake selection.
                if ( !selection.getSelectedElement() )
                    selection.selectElement( element );
            } else {
                element = null;
            }

            // Record down the selected element in the dialog.
            this._.selectedElement = element;

            var data = plugin.parseLinkAttributes(element);
            var $iframe = $(CKEDITOR.dialog.getCurrent().parts.contents.$).find('iframe');
            $iframe.attr("src", editor.config.djangolinkIframeURL + "?_popup=true&" + $.param(data));
            $iframe.hide(0);
            var $dialog_content = $(CKEDITOR.dialog.getCurrent().parts.contents.$);
            $dialog_content.css({'padding': '0'});
            $dialog_content.find('.cke_dialog_page_contents').css('height', '100%')
            $dialog_content.find('.cke_dialog_page_contents table[role=presentation]').css('height', '100%');
            $dialog_content.find('.cke_dialog_ui_vbox_child').css({'padding': '0', 'height': '100%'});
            $dialog_content.find('.cke_dialog_ui_vbox_child iframe').css({'display': 'block'});

            $iframe.unbind('load');
            $iframe.bind('load', function () {
                // tweak UI
                $iframe.show(0);
                var $iframe_content = $(this).contents();
                $iframe_content.find('html, body').scrollTop(0);
                $iframe_content.find('h1').hide().end();
                $iframe_content.find('.submit-row').hide().end();
                $iframe_content.find('#content').css('padding', 0);
                $iframe_content.find('#container').css('min-width', 0).css('padding', 0);

                // form
                var $form = $(this).contents().find('form');
                $form.bind('submit', function(e) {
                    e.preventDefault();
                    // trigger onOK!?
                });

            });
        };

        return dialog;
    } );

    CKEDITOR.tools.extend( CKEDITOR.config, {
        /**
         * where to load the link iframe from
         *
         * @cfg {string} [djangolinkIframeURL='/admin/link/link/add']
         * @member CKEDITOR.config
         */
        djangolinkIframeURL: '/admin/link/link/add/',
        djangolinkVerifyURL: '/admin/link/link/verify/'

    } );

} )(django.jQuery);
