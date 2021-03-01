const defaultState = {
  loggedInUser: {},
};

const userReducer = (state = defaultState, action) => {
  switch (action.type) {
      case 'updateLoggedInUser':
      return {
        ...state,
          loggedInUser: { ...action.payload } || {},
      };
    default:
      return state;
  }
};

export default userReducer;
