import { combineReducers } from 'redux';

// Module Reducers
import dashboardReducer from './modules/dashboard/store';
import userReducer from './modules/auth/store';
import connectionReducer from './modules/connections/store';
import modalReducer from "./modules/modal";
import orchestrationReducer from "./modules/orchestration/store";
import customerProfileReducer from "./modules/customer-data/store";

const rootReducer = combineReducers({
  dashboard: dashboardReducer,
  user: userReducer,
  connections: connectionReducer,
  modal: modalReducer,
  orchestration: orchestrationReducer,
  customerprofiles: customerProfileReducer,
});

export default rootReducer;
