import { combineReducers } from 'redux';

// Module Reducers
import dashboardReducer from './modules/dashboard/store/index';
import userReducer from './modules/auth/store/index';
import connectionReducer from './modules/connections/store/index';
import modalReducer from "./modules/modal/index";
import customerProfileReducer from "./modules/customer-data/store/index";

const rootReducer = combineReducers({
  dashboard: dashboardReducer,
  user: userReducer,
  connections: connectionReducer,
  modal: modalReducer,
  customerprofiles: customerProfileReducer,
});

export default rootReducer;
