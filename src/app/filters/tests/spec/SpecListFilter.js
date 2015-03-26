require([
    'app/filters/ListFilter'
], function(
    ListFilter
) {

    describe('app/filters/ListFilter', function() {
        var testWidget;
        beforeEach(function() {
            testWidget = new ListFilter({
                items: [
                    ['desc1', 'value1'],
                    ['desc2', 'value2']
                ]
            });
        });
        afterEach(function() {
            if (testWidget) {
                if (testWidget.destroy) {
                    testWidget.destroy();
                }

                testWidget = null;
            }
        });
        it('should create a ListFilter', function() {
            expect(testWidget).toEqual(jasmine.any(ListFilter));
        });
        describe('postCreate', function () {
            it('creates bubbles', function () {
                expect(testWidget.buttonContainer.children.length).toBe(2);
                expect(testWidget.buttonContainer.children[1].value).toBe('value2');
            });
        });
        describe('itemClicked', function () {
            it('add to the selected items array', function () {
                testWidget.itemClicked('1');
                expect(testWidget.selectedItems).toEqual(['1']);

                testWidget.itemClicked('2');
                expect(testWidget.selectedItems).toEqual(['1', '2']);
            });
            it('removes if it\'s already been selected', function () {
                testWidget.itemClicked('1');
                testWidget.itemClicked('2');

                testWidget.itemClicked('1');
                expect(testWidget.selectedItems).toEqual(['2']);
            });
        });
    });
});