
/* eslint-disable no-case-declarations */
const defaultState = {
  audienceSummary: [],
  segmentsSummary: [],
};

const orchestrationReducer = (state = defaultState, action) => {
  switch (action.type) {
    case "loadAudienceSummary":
      return {
        ...state,
        dataSources: [...action.payload] || [],
      };
    default:
      return state;
  }
};

export default orchestrationReducer;
