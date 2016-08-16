CKEDITOR.dialog.add( 'django_linkDialog', function( editor ) {
    return {
        title: 'Link Properties',
        minWidth: 400,
        minHeight: 200,
        contents: [
            {
                id: 'tab-basic',
                label: 'Basic Settings',
                elements: [
                    {
                        type: 'text',
                        id: 'django_link',
                        label: 'Abbreviation',
                        validate: CKEDITOR.dialog.validate.notEmpty( "Link field cannot be empty." )
                    },
                ]
            }
        ],
        onOk: function() {
            var dialog = this;
        }
    };
});
