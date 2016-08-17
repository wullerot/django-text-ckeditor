// example from stackoverflow
$(function() {
    (function($) {
        var MutationObserver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver;

        $.fn.attrchange = function(callback) {
            if (MutationObserver) {
                var options = {
                    subtree: false,
                    attributes: true
                };

                var observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(e) {
                        callback.call(e.target, e.attributeName);
                    });
                });

                return this.each(function() {
                    observer.observe(this, options);
                });

            }
        }
    })(jQuery);

    //Now you need to append event listener
    $('body *').attrchange(function(attrName) {

        if(attrName=='class'){
                alert('class changed');
        }else if(attrName=='id'){
                alert('id changed');
        }else{
            //OTHER ATTR CHANGED
        }

    });
});
