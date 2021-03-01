const defaultState = {
  summaryInfo: {},
  recentSegments: [],
};

const dashboardReducer = (state = defaultState, action) => {
  switch (action.type) {
    case 'loadSummary':
      return {
        ...state,
        summaryInfo: {...action.payload},
      };
    case 'updateRecentSegments':
      return {
        ...state,
        recentSegments: [...action.payload],
      };
    default:
      return state;
  }
};

export default dashboardReducer;
