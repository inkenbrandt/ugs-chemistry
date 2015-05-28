define([
    'app/config',
    'app/FilterContainer',
    'app/Grid',
    'app/mapController',

    'dijit/_TemplatedMixin',
    'dijit/_WidgetBase',
    'dijit/_WidgetsInTemplateMixin',

    'dojo/_base/declare',
    'dojo/_base/fx',
    'dojo/_base/lang',
    'dojo/fx',
    'dojo/text!app/templates/App.html',
    'dojo/topic',

    'ijit/widgets/authentication/LoginRegister'
], function (
    config,
    FilterContainer,
    Grid,
    mapController,

    _TemplatedMixin,
    _WidgetBase,
    _WidgetsInTemplateMixin,

    declare,
    baseFx,
    lang,
    coreFx,
    template,
    topic,

    LoginRegister
) {
    return declare([_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
        // summary:
        //      The main widget for the app

        widgetsInTemplate: true,
        templateString: template,
        baseClass: 'app',

        constructor: function () {
            // summary:
            //      first function to fire after page loads
            console.info('app.App::constructor', arguments);

            AGRC.app = this;
        },
        postCreate: function () {
            // summary:
            //      Fires when
            console.log('app.App::postCreate', arguments);

            // set version number
            this.version.innerHTML = AGRC.version;

            this.own(
                new LoginRegister({
                    appName: config.appName,
                    logoutDiv: this.logoutDiv,
                    showOnLoad: false,
                    securedServicesBaseUrl: '??'
                }),
                new FilterContainer(null, this.filterDiv),
                new Grid(null, this.gridDiv)
            );
            mapController.initMap(this.mapDiv);

            this.inherited(arguments);
        },
        startup: function () {
            // summary:
            //      Fires after postCreate when all of the child widgets are finished laying out.
            console.log('app.App::startup', arguments);

            // grid animations
            var open;
            var onEnd = function (opened) {
                open = opened;
                setTimeout(function () {
                    mapController.map.resize();
                }, 50);
            };
            var openAnimation = coreFx.combine([
                baseFx.animateProperty({
                    node: this.gridContainer,
                    properties: {
                        height: config.gridDivHeight,
                        borderWidth: 1
                    },
                    onEnd: lang.partial(onEnd, true)
                }),
                baseFx.animateProperty({
                    node: this.mapDiv,
                    properties: {
                        bottom: config.gridDivHeight
                    }
                })
            ]);
            var closeAnimation = coreFx.combine([
                baseFx.animateProperty({
                    node: this.gridContainer,
                    properties: {
                        height: 0,
                        borderWidth: 0
                    },
                    onEnd: lang.partial(onEnd, false)
                }),
                baseFx.animateProperty({
                    node: this.mapDiv,
                    properties: {
                        bottom: 0
                    }
                })
            ]);

            var toggle = function (animation) {
                if (animation === openAnimation && open) {
                    return true;
                }

                animation.play();
            };
            topic.subscribe(config.topics.toggleGrid, function (show) {
                toggle((show) ? openAnimation : closeAnimation);
            });
        }
    });
});
