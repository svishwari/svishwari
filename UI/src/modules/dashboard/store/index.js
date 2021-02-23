const defaultState = {
  connections: {
    dataSources: 0,
    destinations: 0
  },
  customers: 0,
  orchestrations: {
    segments: 0
  }
};

const dashboardReducer = (state = defaultState, action) => {
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

export default dashboardReducer;
