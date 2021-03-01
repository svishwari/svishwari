/* eslint-disable no-case-declarations */
const defaultState = {
  dataSources: [],
  destinations: [],
};

const connectionReducer = (state = defaultState, action) => {
  switch (action.type) {
    case "loadDataSources":
      return {
        ...state,
        dataSources: [...action.payload] || [],
      };
    case "updateInestionStatus":
      const tmpDS = JSON.parse(JSON.stringify(state.dataSources));
      const _record = tmpDS.filter((item) => item.id === action.payload.id);
      _record[0].ingestionStatus = "InProgess";
      return {
        ...state,
        dataSources: tmpDS,
      };
    case "ingestionComplete":
      const _tmpDS = JSON.parse(JSON.stringify(state.dataSources));
      const _dataSource = _tmpDS.filter(
        (item) => item.id === action.payload.id
      );
      _dataSource[0].ingested = true;
      _dataSource[0].ingestionStatus = true;
      _dataSource[0].recordsIngested = action.payload.recordsIngested;
      _dataSource[0].empty = action.payload.empty;
      _dataSource[0].bogus = action.payload.bogus;
      _dataSource[0].cleansed = action.payload.cleansed;
      return {
        ...state,
        dataSources: _tmpDS,
      };
    case "newDataSourceAdded":
      const originalDS = JSON.parse(JSON.stringify(state.dataSources));
      originalDS.unshift(action.payload);
      return {
        ...state,
        dataSources: originalDS,
      };
    case "dataSourceConnected":
      const __tmpDS = JSON.parse(JSON.stringify(state.dataSources));
      const _tmpobj = __tmpDS.filter((item) => item.id === action.payload.id);
      _tmpobj[0].connectionStatus = "Connected";
      _tmpobj[0].ingested = false;
      return {
        ...state,
        dataSources: __tmpDS,
      };
    case "updateConnectionStatus":
      const ___tmpDS = JSON.parse(JSON.stringify(state.dataSources));
      const __record = ___tmpDS.filter((item) => item.id === action.payload.id);
      __record[0].connectionStatus = "Connecting...";
      return {
        ...state,
        dataSources: ___tmpDS,
      };
    //  Destination related dispatches
    case "loadDestinations":
      return {
        ...state,
        destinations: [...action.payload] || [],
      };
    case "newDestinationAdded":
      const originalDestination = JSON.parse(JSON.stringify(state.destinations));
      originalDestination.unshift(action.payload);
      return {
        ...state,
        destinations: originalDestination,
      };
    case "updateDestinationConnectionStatus":
      const originalDestinationDATA = JSON.parse(JSON.stringify(state.destinations));
      const destinationToBeConnected = originalDestinationDATA.filter((item) => item.id === action.payload.id);
      destinationToBeConnected[0].status = "Connecting...";
      return {
        ...state,
        destinations: originalDestinationDATA,
      };
    case "destinationConnected":
      const originalDestinationDATA2 = JSON.parse(JSON.stringify(state.destinations));
      const connectedDestination = originalDestinationDATA2.filter((item) => item.id === action.payload.id);
      connectedDestination[0].status = "Connected";
      return {
        ...state,
        destinations: originalDestinationDATA2,
      };
    default:
      return state;
  }
};

export default connectionReducer;
