var DjangoLink = ( function( $ ) {
    'use strict';

    var conf = {
        requires: 'dialog,fakeobjects',
        icons: 'DjangoLink',
        hidpi: true,
        onLoad: on_load,
        init: init,
        editLink: edit_link,
        afterInit: init_complete,
    };

    CKEDITOR.plugins.add( 'djangolink', conf );
    CKEDITOR.plugins.djangolink = {
        getLinkAttributes: get_link_attributes,
        getSelectedLink: get_selected_link,
        parseLinkAttributes: parse_link_attributes,
    };

    function init( editor ) {
        var plugin = this;
        var allowed = 'a[!href, data-*]';
        var required = 'a[href]';
        CKEDITOR.dialog.add( 'djangolink', plugin.path + 'dialogs/djangolink.js' );
        editor.addCommand( 'djangolink', {
            allowedContent: allowed,
            requiredContent: required,
            exec: exec_djangolink
        } );
        editor.ui.addButton( 'DjangoLink', {
            label: editor.lang.link.toolbar,
            command: 'djangolink',
            toolbar: 'djangolinks,10',
            icon: 'link'
        } );
        editor.on( 'doubleclick', select_link, null, null, 0 );

        function exec_djangolink() {
            var s = editor.getSelection();
            var el = s.getSelectedElement() || s.getCommonAncestor().getAscendant('a', true);
            plugin.editLink(el, editor);
        };

        function select_link( evt ) {
            var element = CKEDITOR.plugins.link.getSelectedLink( editor ) || evt.data.element;
            if ( !element.isReadOnly() ) {
                if ( element.is( 'a' ) ) {
                    // Pass the link to be selected along with event data.
                    evt.data.dialog = 'djangolink';
                    evt.data.link = element;
                }
            }
            if ( evt.data.dialog in { djangolink: 1, anchor: 1 } && evt.data.link ) {
                editor.getSelection().selectElement( evt.data.link );
            }
        };
    };

    function on_load( ) {
        // Add the CSS styles for anchor placeholders.
        var iconPath = CKEDITOR.getUrl( this.path + 'images' + ( CKEDITOR.env.hidpi ? '/hidpi' : '' ) + '/anchor.png' ),
            baseStyle = 'background:url(' + iconPath + ') no-repeat %1 center;border:1px dotted #00f;background-size:16px;';

        var template = '.%2 a.cke_anchor,' +
            '.%2 a.cke_anchor_empty' +
            ',.cke_editable.%2 a[name]' +
            ',.cke_editable.%2 a[data-cke-saved-name]' +
            '{' +
                baseStyle +
                'padding-%1:18px;' +
                // Show the arrow cursor for the anchor image (FF at least).
                'cursor:auto;' +
            '}' +
            '.%2 img.cke_anchor' +
            '{' +
                baseStyle +
                'width:16px;' +
                'min-height:15px;' +
                // The default line-height on IE.
                'height:1.15em;' +
                // Opera works better with "middle" (even if not perfect)
                'vertical-align:text-bottom;' +
            '}';

        // Styles with contents direction awareness.
        function cssWithDir( dir ) {
            return template.replace( /%1/g, dir == 'rtl' ? 'right' : 'left' ).replace( /%2/g, 'cke_contents_' + dir );
        }

        CKEDITOR.addCss( cssWithDir( 'ltr' ) + cssWithDir( 'rtl' ) );
    };

    function edit_link(element, editor) {
        var $body = $('body');
        var that = this;
        editor.openDialog('djangolink');
    };

    function init_complete( editor ) {
        // init complete
    };


    // Plugin Helpers ---------------------------------------------------------

    /**
     * Converts link data produced by {@link #parseLinkAttributes} into an object which consists
     * of attributes to be set (with their values) and an array of attributes to be removed.
     * This method can be used to compose or to update any link element with the given data.
     *
     * @since 4.4
     * @param {CKEDITOR.editor} editor
     * @param {Object} data Data in {@link #parseLinkAttributes} format.
     * @returns {Object} An object consisting of two keys, i.e.:
     *
     *        {
     *            // Attributes to be set.
     *            set: {
     *                href: 'http://foo.bar',
     *                target: 'bang'
     *            },
     *        }
     *
     */

    function get_link_attributes(editor, data, link_value) {
        var set = { 'data-djangolink': true };
        var excludes = [ '_popup', '_save', 'csrfmiddlewaretoken' ];
        for( var attr in data ) {
            if ( excludes.indexOf( attr ) < 0 && data[ attr ] != null ) {
                set[ 'data-' + attr ] = data[ attr ];
            } else if ( data[ attr ] === null ) {
                set[ 'data-' + attr ] = '';
            }
        }
        set.href = '';
        if ( link_value ) {
            set.href = link_value;
        }
        return {
            set: set,
            removed: CKEDITOR.tools.objectKeys( [] )
        };
    };

    function get_selected_link( editor ) {
        var selection = editor.getSelection();
        var selectedElement = selection.getSelectedElement();
        if ( selectedElement && selectedElement.is( 'a' ) ) {
            return selectedElement;
        }
        var range = selection.getRanges()[ 0 ];
        if ( range ) {
            range.shrink( CKEDITOR.SHRINK_TEXT );
            return editor.elementPath( range.getCommonAncestor() ).contains( 'a', 1 );
        }
        return null;
    };

    function parse_link_attributes( element ) {
        /**
        * Parses attributes of the link element and returns an object representing
        * the current state (data) of the link. This data format is a plain object accepted
        * e.g. by the Link dialog window and {@link #getLinkAttributes}.
        *
        * **Note:** Data model format produced by the parser must be compatible with the Link
        * plugin dialog because it is passed directly to {@link CKEDITOR.dialog#setupContent}.
        *
        * @since 4.4
        * @param {CKEDITOR.editor} editor
        * @param {CKEDITOR.dom.element} element
        * @returns {Object} An object of link data.
        **/
        if (!element || !element.$.attributes) {
            return {};
        }
        var data = {};
        $.each(element.$.attributes, function(index, attribute) {
            var key = attribute.name.substr('data-'.length);
            data[key] = attribute.value;
        });
        return data
    };


    // Utilities --------------------------------------------------------------

    function unescapeSingleQuote( str ) {
        return str.replace( /\\'/g, '\'' );
    };

    function escapeSingleQuote( str ) {
        return str.replace( /'/g, '\\$&' );
    };

})( django.jQuery );
