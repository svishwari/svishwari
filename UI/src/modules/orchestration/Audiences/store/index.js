const defaultState = {
  audiences: [],
};

const audiencesReducer = (state = defaultState, action) => {
  switch (action.type) {
    case 'updateAudiences':
      return {
        ...state,
        audiences: [...action.payload],
      };
    default:
      return state;
  }
};

export default audiencesReducer;
