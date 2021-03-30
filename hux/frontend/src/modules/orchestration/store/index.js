/* eslint-disable no-case-declarations */
const defaultState = {
  audience: [],
  audiences: [],
  segments: [],
  segmentSummary: {},
};

const orchestrationReducer = (state = defaultState, action) => {
  switch (action.type) {
      case "loadAudiences":
          return {
              ...state,
              audiences: [...action.payload] || [],
          };

      case "loadSegments":
          return {
              ...state,
              segments: [...action.payload] || [],
            };
      case "addSegment":
        return {
            ...state,
            segments: [action.payload,...state.segments] || [],
          };
      case "removeSegment":
        const originalSegments3 = JSON.parse(JSON.stringify(state.segments));
        const filteredSegments3 = originalSegments3.filter((item) => item.id !== action.payload.id);
        return {
            ...state,
            segments: filteredSegments3 || [],
        };
      case "updateDeliverStatus":
        const originalSegments = JSON.parse(JSON.stringify(state.segments));
        const filteredSegments = originalSegments.filter((item) => item.id === action.payload.id);
        filteredSegments[0].deliverStatus = "Delivering...";
        return {
          ...state,
          segments: originalSegments,
        };
      case "segmentDelivered":
        const originalSegments2 = JSON.parse(JSON.stringify(state.segments));
        const filteredSegments2 = originalSegments2.filter((item) => item.id === action.payload.id);
        filteredSegments2[0].deliverStatus = "Delivered";
        return {
          ...state,
          segments: originalSegments2,
        };
      case "loadSegmentSummary":
        return {
          ...state,
          segmentSummary: action.payload || {},
        };
      default:
          return state;
  }
};

export default orchestrationReducer;
