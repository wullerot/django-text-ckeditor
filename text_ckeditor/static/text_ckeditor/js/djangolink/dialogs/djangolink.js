var DjangoLinkDialog = ( function( $ ) {
    'use strict';

    var iframe_html = '<iframe style="position:static; width:100%; height:100%; border:none;" />';

    CKEDITOR.dialog.add('djangolink', djangolink_dialog );

    function djangolink_dialog( instance ) {
        var anchors;
        var editor = instance;
        var plugin = CKEDITOR.plugins.djangolink;
        var iframeURL = editor.config.djangolinkIframeURL;
        var verifyURL = editor.config.djangolinkVerifyURL;
        var dialogInstance = {
            onOk: on_ok,
            onShow: on_show,
            title: 'Link',
            width: 800,
            height: 400,
            minHeight: 300,
            contents: [ { elements: [ { type: 'html', html: iframe_html } ] } ]
        };

        function on_ok() {
            var data = {};
            var dialog = this;
            var $iframe = $( dialog.parts.contents.$ ).find('iframe').contents();
            var $form = $iframe.find('form');
            var $fields = $form.find("input, select");
            for ( var i = 0; i < $fields.length; i++ ) {
                data[ $fields[ i ].name ] = $fields[ i ].value;
            }
            $.ajax( {
                method: 'post',
                url: verifyURL,
                data: data,
                success: success
            } );

            function success( response, status, xhr ) {
                // django form error ------------------------------------------
                if ( response.valid != 'true') {
                    show_form_errors( $form, response );
                    return false;
                }
                // no form errors ---------------------------------------------
                var selection = editor.getSelection();
                var element = dialog.getSelectedElement()
                var attributes = plugin.getLinkAttributes( editor, response.data, response.link_value );
                if ( !element ) {
                    insert_link_element( editor, selection, attributes );
                } else {
                    edit_link_element( selection, element, attributes, data )
                }
                $( 'body', $iframe ).remove();
                CKEDITOR.dialog.getCurrent().hide();
            };

            return false;
        };

        function on_show() {
            var dialog = this;
            var editor = this.getParentEditor();
            var selection = editor.getSelection();
            var element = plugin.getSelectedLink( editor );
            if ( element && element.hasAttribute( 'href' ) ) {
                if ( !selection.getSelectedElement() ) {
                    selection.selectElement( element );
                }
            } else {
                element = null;
            }

            // Record down the selected element in the dialog.
            // TODO find a proper way to do this
            dialog._.selectedElement = element;

            var data = plugin.parseLinkAttributes( element );
            var $dialog = $( dialog.parts.contents.$ );
            var $iframe = $( 'iframe', $dialog );
            $iframe.attr( { src: iframeURL + "?_popup=true&" + $.param( data ) } );
            $iframe.unbind( 'load' ).hide();
            $dialog.css( { 'padding': '0' } );
            $( '.cke_dialog_page_contents, table[role=presentation]', $dialog ).css( { height: '100%' } );
            $( '.cke_dialog_ui_vbox_child', $dialog ).css( { padding: 0, height: '100%' } );
            $( '.cke_dialog_ui_vbox_child iframe', $dialog ).css( { display: 'block' } );

            $iframe.bind('load', function () {
                // tweak UI
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
                $iframe.show(0);

            });
        };

        return dialogInstance;
    };

    function edit_link_element( selection, element, attributes, data ) {
        var href = element.data( 'cke-saved-href' );
        var textView = element.getHtml();

        element.setAttributes( attributes.set );
        element.removeAttributes( attributes.removed );

        // Update text view when user changes protocol (#4612).
        if ( href == textView || data.type == 'email' && textView.indexOf( '@' ) != -1 ) {
            // Short mailto link text view (#5736).
            element.setHtml( data.type == 'email' ? data.email.address : attributes.set[ 'data-cke-saved-href' ] );

            // We changed the content, so need to select it again.
            selection.selectElement( element );
        }
    }

    function insert_link_element( editor, selection, attributes ) {
        var range = selection.getRanges()[ 0 ];
        if ( range.collapsed ) {
            // Nothing selected insert placeholder text
            insert_link_text( editor, range );
        }
        // Apply style.
        var style = new CKEDITOR.style( {
            element: 'a',
            attributes: attributes.set
        } );

        style.type = CKEDITOR.STYLE_INLINE;
        style.applyToRange( range, editor );
        range.select();
    };

    function insert_link_text( editor, range) {
        var text = new CKEDITOR.dom.text('link', editor.document );
        range.insertNode(text);
        range.selectNodeContents(text);
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

} )(django.jQuery);
