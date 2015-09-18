require([
    'app/Grid',

    'dojo/dom-class',
    'dojo/dom-construct'
], function (
    WidgetUnderTest,

    domClass,
    domConstruct
) {
    describe('app/Grid', function () {
        var widget;
        var destroy = function (widget) {
            widget.destroyRecursive();
            widget = null;
        };

        beforeEach(function () {
            widget = new WidgetUnderTest(null, domConstruct.create('div', null, document.body));
            widget.startup();
        });

        afterEach(function () {
            if (widget) {
                destroy(widget);
            }
        });

        describe('Sanity', function () {
            it('should create a Grid', function () {
                expect(widget).toEqual(jasmine.any(WidgetUnderTest));
            });
        });
        describe('populateGrid', function () {
            it('creates the correct query for results table', function () {
                domClass.remove(widget.stationsTab, 'active');

                // query on the stations table
                widget.populateGrid('Blah = 2');

                expect(widget.resultQuery.where).toBe('StationId IN (SELECT StationId FROM Stations WHERE Blah = 2)');

                // query on results tabls
                widget.populateGrid("StationId IN (SELECT StationId FROM Results WHERE SampleDate >= '01/01/2015' AND SampleDate <= '02/01/2015')");

                expect(widget.resultQuery.where).toBe("SampleDate >= '01/01/2015' AND SampleDate <= '02/01/2015'");
            });
        });
    });
});
