require([
    'app/config',
    'app/filters/FreeTypeFilter',

    'dojo/dom-construct'
], function (
    config,
    WidgetUnderTest,

    domConstruct
) {
    describe('app/filters/FreeTypeFilter', function () {
        var widget;
        var destroy = function (widget) {
            widget.destroyRecursive();
            widget = null;
        };

        beforeEach(function () {
            widget = new WidgetUnderTest({
                fieldName: 'FieldName'
            }, domConstruct.create('div', null, document.body));
            widget.startup();
        });

        afterEach(function () {
            if (widget) {
                destroy(widget);
            }
        });

        describe('Sanity', function () {
            it('should create a FreeTypeFilter', function () {
                expect(widget).toEqual(jasmine.any(WidgetUnderTest));
            });
        });
        describe('getQuery', function () {
            it('returns the appropriate query when a value is applied', function () {
                widget.txtBox.value = 'blah';
                widget.onApplyClick();

                expect(widget.getQuery()).toEqual('FieldName = \'blah\'');
            });
            it('returns undefined if no query has been applied', function () {
                widget.txtBox.value = 'blah';

                expect(widget.getQuery()).toBeUndefined();
            });
            it('returns the appropriate related table query form', function () {
                widget.relatedTableQuery = true;
                widget.txtBox.value = 'blah';
                widget.onApplyClick();

                expect(widget.getQuery()).toEqual(config.queryByResults + 'FieldName = \'blah\')');
            });
        });
    });
});
