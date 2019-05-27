var LinkType = ( function() {
    'use strict';

    document_ready( init );

    function init() {
        var i;
        var elements = $( 'form' );
        for( i=0; i < elements.length; i++ ){
            init_form( elements[ i ] );
        }
    };

    function init_form( form ) {
        var i;
        var fieldsets = $( 'fieldset', form );
        for( i=0; i < fieldsets.length; i++ ){
            if( $( '.field-link_type select', fieldsets[ i ] ).length == 1 ) {
                init_fieldset( fieldsets[ i ] );
            }
        }
    };

    function init_fieldset( fs ) {
        var i, u, v, $t;
        var select = $( '.field-link_type select', fs )[0]
        fs._select = select;
        select._fieldset = fs;
        for( i=0; i < fs._select.options.length; i++ ){
            if( fs._select.options[ i ].value ) {
                v = fs._select.options[ i ].value;
                $t = $( '[class*="field-' + v + '"]' );
                if( $t.length > 0 ) {
                    add_class( $t, 'linktype__row' );
                    add_class( $t, 'linktype__' + v );
                }
            }
        }
        select_changed( u, select );
        select.addEventListener( 'change', select_changed )
    };

    function select_changed( e, select ) {
        var select = e ? this : select;
        add_class(
            $( '.linktype__row', select._fieldset ),
            'linktype__hidden'
        );
        if( select.value ) {
            remove_class(
                $( '.linktype__' + select.value, select._fieldset ),
                'linktype__hidden'
            );
        }
    };


    // Utilities -------------------------------------------------------------

    function $( selector, parent ) {
        var root = parent ? parent : document;
        var query = root.querySelectorAll( selector );
        return Array.prototype.slice.call( query );
    };

    function document_ready( fn ) {
        var state = document.readyState;
        if ( typeof fn !== 'function' ) {
            return;
        }
        if (  state === 'interactive' || state === 'complete' ) {
            return fn();
        }
        document.addEventListener( 'DOMContentLoaded', fn, false );
    };

    function add_class( elements, class_name ) {
        var i;
        if ( typeof( elements ) === 'string' ) {
            elements = $( elements );
        }
        if ( !elements ) {
            return;
        }
        // add class to all chosen elements
        for ( i=0; i < elements.length; i++ ) {
            // check if it has already the given class
            if ( ( ' ' + elements[ i ].className + ' ').indexOf(' ' + class_name + ' ' ) < 0 ) {
                elements[ i ].className += ' ' + class_name;
            }
        }
    };

    function remove_class( elements, class_name ) {
        var i;
        if ( typeof( elements ) === 'string' ) {
            elements = $( elements );
        }
        if ( !elements ) {
            return;
        }
        // create pattern to find class name
        var reg = new RegExp( '(^| )' + class_name + '($| )', 'g' );
        // remove class from all chosen elements
        for ( i=0; i < elements.length; i++ ) {
            elements[ i ].className = elements[ i ].className.replace( reg, ' ' );
        }
    };
} )();
