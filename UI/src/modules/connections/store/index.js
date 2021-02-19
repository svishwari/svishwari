const defaultState = {
  dataSources: [],
  destinations: [],
};

const connectionReducer = (state = defaultState, action) => {
  switch (action.type) {
    case "loadDataSources":
      return {
        ...state,
        dataSources: [...action.payload] || []
      }
    case "loadDataExtensions":
      return {
        ...state,
        destinations: [...action.payload]
      }
    case "updateInestionStatus":
      let _record = state.dataSources.filter(item => item.id === action.payload.id)
      _record[0].ingestionStatus = "InProgess"
      console.log(state.dataSources)
      // console.log(action.payload, _record)
      return {
        ...state
      }
    case "ingestionComplete":
      let _dataSource = state.dataSources.filter(item => item.id === action.payload.id)
      _dataSource[0].ingested=true
      _dataSource[0].ingestionStatus = true
      _dataSource[0].recordsIngested = action.payload.recordsIngested
      _dataSource[0].empty = action.payload.empty
      _dataSource[0].bogus = action.payload.bogus
      _dataSource[0].cleansed = action.payload.cleansed
      
      return {
        ...state
      }
    default:
      return state
  }
};

export default connectionReducer;
