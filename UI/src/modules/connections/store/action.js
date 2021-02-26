// import { getRequest } from "../../../hooks/apiClient";
// import slugs from "../../../resources/slugs";

const setDataSources = (payload) => ({ type: "loadDataSources", payload });
const setDestinations = (payload) => ({ type: "loadDestinations", payload });
const ingestionCompleted = (payload) => ({
  type: "ingestionComplete",
  payload,
});
const dataSourceConnected = (payload) => ({
  type: "dataSourceConnected",
  payload,
});
const newDataSourceAdded = (payload) => ({
  type: "newDataSourceAdded",
  payload,
});

export const logUserOut = () => ({ type: "LOG_OUT" });

// Methods
const fetchDataSources = () => async (dispatch) => {
  await new Promise((done) => setTimeout(() => done(), 2000));
  const response = [
    {
      id: "602ec30dc920d42f1c4c5d22",
      fileName: "File Name 1",
      source: "Client",
      lastUpdated: "03/26/19 05:04PM",
      connectionStatus: "Not Connected",
      ingested: true,
      ingestionStatus: true,
      recordsIngested: 189,
      empty: 148,
      bogus: 43,
      cleansed: 9,
      starred: true,
    },
    {
      id: "602ec30e3d14a94dc1f30e97",
      fileName: "File Name 2",
      source: "Client",
      lastUpdated: "05/08/20 07:37PM",
      connectionStatus: "Connected",
      ingested: true,
      ingestionStatus: true,
      recordsIngested: 2818,
      empty: 212,
      bogus: 45,
      cleansed: 1,
      starred: true,
    },
    {
      id: "602ec30ed4a16f2941a2e37a",
      fileName: "File Name 3",
      source: "Client",
      lastUpdated: "12/13/20 11:57PM",
      connectionStatus: "Connected",
      ingested: false,
      ingestionStatus: false,
      recordsIngested: 3779,
      empty: 393,
      bogus: 21,
      cleansed: 26,
      starred: true,
    },
    {
      id: "602ec30eb4bd75c785ecc523",
      fileName: "File Name 4",
      source: "Client",
      lastUpdated: "09/02/20 08:17AM",
      connectionStatus: "Not Connected",
      ingested: true,
      ingestionStatus: true,
      recordsIngested: 324,
      empty: 106,
      bogus: 46,
      cleansed: 17,
    },
    {
      id: "602ec30e74c166dc2623be9e",
      fileName: "File Name 5",
      source: "Amazon S3",
      lastUpdated: "02/23/19 09:12PM",
      connectionStatus: "Not Connected",
      ingested: true,
      ingestionStatus: true,
      recordsIngested: 3641,
      empty: 278,
      bogus: 21,
      cleansed: 15,
      starred: true,
    },
    {
      id: "602ec30ef17d5ba0428cbb5e",
      fileName: "File Name 6",
      source: "Amazon S3",
      lastUpdated: "12/07/19 01:21PM",
      connectionStatus: "Connected",
      ingested: true,
      ingestionStatus: true,
      recordsIngested: 896,
      empty: 316,
      bogus: 21,
      cleansed: 19,
      starred: true,
    },
    {
      id: "602ec30e8b941a5dcd05c61d",
      fileName: "File Name 7",
      source: "Client",
      lastUpdated: "01/30/20 01:19AM",
      connectionStatus: "Not Connected",
      ingested: true,
      ingestionStatus: true,
      recordsIngested: 500,
      empty: 174,
      bogus: 40,
      starred: true,
      cleansed: 10,
    },
    {
      id: "602ec30ed02a9acce5f1e477",
      fileName: "File Name 8",
      source: "Amazon S3",
      lastUpdated: "07/16/19 04:41PM",
      connectionStatus: "Connected",
      ingested: true,
      ingestionStatus: true,
      recordsIngested: 715,
      empty: 43,
      bogus: 20,
      cleansed: 16,
    },
    {
      id: "602ec30e8729cc8daca83fef",
      fileName: "File Name 9",
      source: "Amazon S3",
      lastUpdated: "07/24/20 09:23AM",
      connectionStatus: "Connected",
      ingested: false,
      ingestionStatus: false,
      recordsIngested: 684,
      empty: 349,
      bogus: 29,
      cleansed: 3,
    },
    {
      id: "602ec30eeba7526a18d2db70",
      fileName: "File Name 10",
      source: "Client",
      lastUpdated: "11/27/19 06:16AM",
      connectionStatus: "Not Connected",
      ingested: true,
      ingestionStatus: true,
      recordsIngested: 484,
      empty: 53,
      bogus: 21,
      cleansed: 19,
      starred: true,
    },
    {
      id: "602ec30eeba7526a18d2db23",
      fileName: "File Name 11",
      source: "Client",
      lastUpdated: "11/27/19 06:16AM",
      connectionStatus: "Not Connected",
      ingested: true,
      ingestionStatus: true,
      recordsIngested: 484,
      empty: 53,
      bogus: 21,
      cleansed: 19,
    },
    {
      id: "602ec30eeba3226a18d2db23",
      fileName: "File Name 12",
      source: "Client",
      lastUpdated: "11/27/19 06:16AM",
      connectionStatus: "Not Connected",
      ingested: true,
      ingestionStatus: true,
      recordsIngested: 484,
      empty: 53,
      bogus: 21,
      cleansed: 19,
    },
  ];
  dispatch(setDataSources(response));
};
const triggerIngestion = (id) => async (dispatch) => {
  await new Promise((done) => setTimeout(() => done(), 5000));
  const response = {
    id,
    recordsIngested: Math.floor(Math.random() * (10000 + 1) + 350),
    empty: Math.floor(Math.random() * (100 + 1) + 50),
    bogus: Math.floor(Math.random() * (1000 + 1) + 150),
    cleansed: Math.floor(Math.random() * (1000 + 1) + 350),
  };
  dispatch(ingestionCompleted(response));
};

const triggerConnectionCheck = (id) => async (dispatch) => {
  await new Promise((done) => setTimeout(() => done(), 3000));
  const response = {
    id,
    status: "Connected",
  };
  dispatch(dataSourceConnected(response));
};

const addNewDataSource = () => async (dispatch) => {
  await new Promise((done) => setTimeout(() => done(), 800));
  const response = {
    id: Math.random().toString(16).slice(2),
    fileName: "Pendalton source",
    source: "Amazon S3",
    lastUpdated: "03/26/19 05:04PM",
    connectionStatus: "Not Connected",
    ingested: false,
  };
  dispatch(newDataSourceAdded(response));
};


//  Destination related actions
const fetchDestinations = () => async (dispatch) => {
  await new Promise((done) => setTimeout(() => done(), 2000));
  const destinationResponse = [
    {
      id: "602ec30dc920d42f1c4c5d22",
      destination: "fb",
      status: "Not Connected",
      destinationName: "File Name 1",
      account: "Pendleton",
      lastUpdated: "03/26/19 05:04PM",
    },
    {
      id: "602ec30e3d14a94dc1f30e97",
      destination: "ga",
      status: "Not Connected",
      destinationName: "File Name 2",
      account: "Pendleton",
      lastUpdated: "03/26/19 05:04PM",
    },
    {
      id: "602ec30ed4a16f2941a2e37a",
      destination: "sfmc",
      status: "Not Connected",
      destinationName: "File Name 3",
      account: "Pendleton",
      lastUpdated: "03/26/19 05:04PM",
    },
    {
      id: "602ec30eb4bd75c785ecc523",
      destination: "ga",
      status: "Connected",
      destinationName: "File Name 4",
      account: "Pendleton",
      lastUpdated: "03/26/19 05:04PM",
    },
    {
      id: "602ec30e74c166dc2623be9e",
      destination: "fb",
      status: "Not Connected",
      destinationName: "File Name 5",
      account: "Pendleton",
      lastUpdated: "03/26/19 05:04PM",
    },
    {
      id: "602ec30ef17d5ba0428cbb5e",
      destination: "fb",
      status: "Not Connected",
      destinationName: "File Name 6",
      account: "Pendleton",
      lastUpdated: "03/26/19 05:04PM",
    },
    {
      id: "602ec30e8b941a5dcd05c61d",
      destination: "sfmc",
      status: "Connected",
      destinationName: "File Name 7",
      account: "Pendleton",
      lastUpdated: "03/26/19 05:04PM",
    },
    {
      id: "602ec30ed02a9acce5f1e477",
      destination: "sfmc",
      status: "Not Connected",
      destinationName: "File Name 8",
      account: "Pendleton",
      lastUpdated: "03/26/19 05:04PM",
    }
  ];
  dispatch(setDestinations(destinationResponse));
}
const destinationConnected = (payload) => ({
  type: "destinationConnected",
  payload,
});

const triggerDestinationConnectionCheck = (id) => async (dispatch) => {
  await new Promise((done) => setTimeout(() => done(), 3000));
  const response = {
    id,
    status: "Connected",
  };
  dispatch(destinationConnected(response));
};


export {
  fetchDataSources,
  triggerIngestion,
  triggerConnectionCheck,
  addNewDataSource,
  fetchDestinations,
  triggerDestinationConnectionCheck,
};
