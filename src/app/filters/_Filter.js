define([
    'dijit/_TemplatedMixin',
    'dijit/_WidgetBase',
    'dijit/_WidgetsInTemplateMixin',

    'dojo/_base/declare',
    'dojo/_base/query',
    'dojo/Evented',
    'dojo/on',

    'dojo-bootstrap/Collapse'
], function(
    _TemplatedMixin,
    _WidgetBase,
    _WidgetsInTempalteMixin,

    declare,
    query,
    Evented,
    on
) {
    return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTempalteMixin, Evented], {
        // description:
        //      A base class for filters that are included in FilterContainer


        // Properties to be sent into constructor

        constructor: function () {
            // summary:
            //      apply some defaults
            console.log('app/_Filter:constructor', arguments);
        
            this.baseClass += ' panel panel-default';
        },
        postCreate: function () {
            // summary:
            //      description
            console.log('app/_Filter:postCreate', arguments);
        
            query(this.body).collapse({
                parent: this.parent,
                toggle: false
            });

            var that = this;
            on(this.heading, 'click', function (evt) {
                if (evt.srcElement !== that.closeBtn &&
                    evt.srcElement !== that.closeSpan) {
                    query(that.body).collapse('toggle');
                }
            });

            this.inherited(arguments);
        },
        remove: function () {
            // summary:
            //      description
            console.log('app/_Filter:remove', arguments);
        
            this.clear();

            this.emit('removed', this);
        },
        open: function () {
            // summary:
            //      description
            console.log('app/_Filter:open', arguments);
        
            query(this.body).collapse('show');
        }
    });
});