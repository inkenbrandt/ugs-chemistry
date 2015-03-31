require([
    'app/filters/DateFilter',

    'dojo/dom-construct'
], function(
    WidgetUnderTest,

    domConstruct
) {
    describe('app/filters/DateFilter', function() {
        var widget;
        var destroy = function (widget) {
            widget.destroyRecursive();
            widget = null;
        };

        beforeEach(function() {
            widget = new WidgetUnderTest({
                fieldName: 'FieldName',
                title: 'hello'
            }, domConstruct.create('div', null, document.body));
            widget.startup();
        });

        afterEach(function() {
            if (widget) {
                destroy(widget);
            }
        });

        describe('Sanity', function() {
            it('should create a DateFilter', function() {
                expect(widget).toEqual(jasmine.any(WidgetUnderTest));
            });
        });
        describe('getQuery', function () {
            it('builds a where clause', function () {
                widget.fromDate.value = '03/30/2015';
                widget.from.update();
                widget.toDate.value = '03/27/2015';
                widget.to.update();

                var result = widget.getQuery();

                expect(result).toBe("StationId IN (SELECT StationId FROM Results WHERE " +
                    "FieldName >= date '2015-03-30' AND FieldName <= date '2015-03-27')");
            });
            it('returns undefined if there are not valid dates', function () {
                expect(widget.getQuery()).toBeUndefined();
            });
        });
    });
});
