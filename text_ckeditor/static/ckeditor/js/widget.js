var CKEditorWidget = ( function( $ ) {

    var $textareas;
    var $widgets;

    var uicolor = '#ffffff';
    var skin = 'minimalist';
    var empty = '__prefix__';
    var not_implemented = 'inline admin not implemented yet';

    $('document').ready(ready);

    function ready() {
        $textareas = $('.textarea-ckeditor');
        $textareas.each( init );
    };

    function init() {
        var ta = this
        var $ta = $(this);
        if ( ta.id.indexOf( empty ) >= 0 ) {
            console.error( ta.id, not_implemented );
            return ta;
        }
        var conf = {
            height: $ta.data('height') || $ta.height(),
            width: $ta.data('width') || $ta.width(),
            skin: $ta.data('skin') || skin,
            uiColor: $ta.data('uicolor') || uicolor,
            extraPlugins: 'django_link',
            toolbar: [
                ['Bold', 'Italic'],
                ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
                ['NumberedList', 'BulletedList'],
                ['Django_link'],
                ['Source'],
                ['Maximize']
            ]
        }
        CKEDITOR.plugins.addExternal( 'django_link', '/static/ckeditor/plugins/django_link/' );
        CKEDITOR.replace(ta.id, conf);
    };
})( django.jQuery );
