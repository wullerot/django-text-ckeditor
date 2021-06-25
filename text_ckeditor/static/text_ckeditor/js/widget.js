var CKEditorWidget = (function ($) {

    var $textareas;
    var $widgets;

    var uicolor = '#ffffff';
    var skin = 'flat';
    var empty = '__prefix__';
    var extra_plugins = '';
    var djangolink_iframe_url = '';
    var djangolink_verify_url = '';
    var djangoimage_iframe_url = '';
    var djangoimage_verify_url = '';
    var not_implemented = 'inline admin not implemented yet';

    $('document').ready(ready);

    function ready() {
        $textareas = $('.textarea-ckeditor');
        $textareas.each(init);
    };

    function init() {
        var ta = this
        var $ta = $(this);
        if (ta.id.indexOf(empty) >= 0) {
            console.error(ta.id, not_implemented);
            return ta;
        }
        var conf = {
            height: $ta.data('height') || $ta.height(),
            width: $ta.data('width') || $ta.width(),
            skin: $ta.data('skin') || skin,
            uiColor: $ta.data('uicolor') || uicolor,
            djangolinkIframeURL: $ta.data('djangolinkiframeurl') || djangolink_iframe_url,
            djangolinkVerifyURL: $ta.data('djangolinkverifyurl') || djangolink_verify_url,
            djangoimageIframeURL: $ta.data('djangoimageiframeurl') || djangoimage_iframe_url,
            djangoimageVerifyURL: $ta.data('djangoimageverifyurl') || djangoimage_verify_url,
            extraPlugins: $ta.data('extraplugins') || extra_plugins,
            toolbar: $ta.data('toolbar') || [
                ['Bold', 'Italic'],
                ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
                ['NumberedList', 'BulletedList'],
                ['Link', 'Unlink'],
                ['Source'],
                ['Maximize']
            ]
        };
        var ckeditor = CKEDITOR.replace(ta.id, conf);
        ckeditor.on('instanceReady', ckeditor_ready);
        ckeditor.config.djangolinkIframeURL

        function ckeditor_ready(e) {
            if ($ta.data('fullscreen')) {
                ckeditor.execCommand('maximize');
            }
        };
    };
})(django.jQuery);
