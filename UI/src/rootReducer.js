import { combineReducers } from 'redux';

// Module Reducers
import dashboardReducer from './modules/dashboard/store/index';
import userReducer from './modules/auth/store/index';
import connectionReducer from './modules/connections/store/index';
import modalReducer from "./modules/modal/index";
import audiencesReducer from './modules/orchestration/audiences/store/index';

const rootReducer = combineReducers({
  dashboard: dashboardReducer,
  user: userReducer,
  connections: connectionReducer,
  audiences: audiencesReducer,
  modal: modalReducer,
});

export default rootReducer;
