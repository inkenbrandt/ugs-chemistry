define([
    'app/filters/_Filter',

    'dojo/_base/declare',
    'dojo/_base/lang',
    'dojo/dom-class',
    'dojo/dom-construct',
    'dojo/on',
    'dojo/query',
    'dojo/text!app/filters/templates/ListFilter.html',

    'dojo-bootstrap/Button',
    'xstyle/css!app/filters/resources/ListFilter.css'
], function(
    _Filter,

    declare,
    lang,
    domClass,
    domConstruct,
    on,
    query,
    template
) {
    return declare([_Filter], {
        // description:
        //      A control for filtering by a defined set of choices.
        //      Allows selection of one or more choices.

        templateString: template,

        // selectedItems: String[]
        //      The currently selected items
        selectedItems: null,


        // properties passed in via the constructor

        // items: [String, String][]
        //      description, value pairs
        items: null,

        constructor: function () {
            // summary:
            //      apply base class
            console.log('app/ListFilter:constructor', arguments);
        
            this.baseClass += ' list-filter';
            this.selectedItems = [];
        },
        postCreate: function () {
            // summary:
            //      build bubbles
            console.log('app/filters/ListFilter:postCreate', arguments);
        
            var that = this;
            this.items.forEach(function (item) {
                domConstruct.create('button', {
                    innerHTML: item[0],
                    value: item[1],
                    'class': 'btn btn-default btn-xs',
                    'data-toggle': 'button',
                    'onclick': lang.partial(lang.hitch(that, 'itemClicked'), item[1])
                }, that.buttonContainer);
            });

            this.inherited(arguments);
        },
        clear: function () {
            // summary:
            //      unselects all buttons
            console.log('app/filters/ListFilter:clear', arguments);
        
            query('.btn', this.buttonContainer).forEach(function (btn) {
                domClass.remove(btn, 'active');
                btn.setAttribute('aria-pressed', false);
            });

            this.numSpan.innerHTML = 0;
            this.selectedItems = [];
        },
        itemClicked: function (id) {
            // summary:
            //      description
            // id: String
            //      id of the item that was clicked
            console.log('app/filters/ListFilter:itemClicked', arguments);
        
            var index = this.selectedItems.indexOf(id);
            if (index === -1) {
                this.selectedItems.push(id);
            } else {
                this.selectedItems.splice(index, 1);
            }

            this.numSpan.innerHTML = this.selectedItems.length;
        }
    });
});