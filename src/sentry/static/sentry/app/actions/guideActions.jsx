import Reflux from 'reflux';

let GuideActions = Reflux.createActions([
  'closeGuide',
  'fetchSucceeded',
  'nextStep',
  'openDrawer',
  'registerAnchor',
  'unregisterAnchor',
]);

export default GuideActions;
