import { combineReducers } from "redux";

// Module Reducers
import dashboardReducer from "./modules/dashboard/store/index";
import userReducer from "./modules/auth/login/store/index";
import connectionReducer from "./modules/connections/store/index";

const rootReducer = combineReducers({
  dashboardReducer,
  user: userReducer,
  connections: connectionReducer,
});

export default rootReducer;
