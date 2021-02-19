const defaultState = {
  dataSources: [],
  destinations: [],
}

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
      let tmpDS = JSON.parse(JSON.stringify(state.dataSources));
      let _record = tmpDS.filter(item => item.id === action.payload.id)
      _record[0].ingestionStatus = "InProgess"
      return {
        ...state,
        dataSources: tmpDS
      }
    case "ingestionComplete":
      let _tmpDS = JSON.parse(JSON.stringify(state.dataSources));
      let _dataSource = _tmpDS.filter(item => item.id === action.payload.id)
      _dataSource[0].ingested=true
      _dataSource[0].ingestionStatus = true
      _dataSource[0].recordsIngested = action.payload.recordsIngested
      _dataSource[0].empty = action.payload.empty
      _dataSource[0].bogus = action.payload.bogus
      _dataSource[0].cleansed = action.payload.cleansed
      return {
        ...state,
        dataSources: _tmpDS
      }
    case "addNew":
      state.datasources.Push(action.Payload);
      return state
    case "dataSourceConnected":
      let __tmpDS = JSON.parse(JSON.stringify(state.dataSources));
      let _tmpobj = __tmpDS.filter(item => item.id === action.payload.id)
      _tmpobj[0].connectionStatus = "connected"
      _tmpobj[0].ingested = false
      return {
        ...state,
        dataSources: __tmpDS
      }
    case "updateConnectionStatus":
      let ___tmpDS = JSON.parse(JSON.stringify(state.dataSources));
      let __record = ___tmpDS.filter(item => item.id === action.payload.id)
      __record[0].connectionStatus = "connecting..."
      return {
        ...state,
        dataSources: ___tmpDS
      }
    default:
      return state
  }
};

export default connectionReducer;
