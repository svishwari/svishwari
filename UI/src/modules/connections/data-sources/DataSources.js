import { Chip, IconButton } from "@material-ui/core";
import React from "react";
import { connect, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import CTDataGrid from "../../../components/Table/CTDataGrid";
import { fetchDataSources, triggerIngestion, triggerConnectionCheck } from "../store/action";
const markIngestionStatus = (payload) => ({ type: "updateInestionStatus", payload });
const markConnecting = (payload) => ({ type: "updateConnectionStatus", payload });


const DataSources = (props) => {
  //this hook allows us to access the dispatch function
  const dispatch = useDispatch();
  const columns = [
    {
      field: "fileName",
      headerName: "File Name",
      flex: 0.2,
      renderCell: (params) => (
        <Link to="#">
          {params.getValue("fileName")}{" "}
          <span
            className="iconify"
            data-icon="mdi:open-in-new"
            data-inline="false"
          ></span>
        </Link>
      ),
    },
    {
      field: "source",
      headerName: "Source",
      flex: 0.1
    },
    {
      field: "lastUpdated",
      headerName: "Last Updated",
      flex: 0.15
    },
    {
      field: "connectionStatus",
      headerName: "Connection Status",
      flex: 0.15,
      renderCell: (params) => {
        const triggerConnection = () => {
          const payload = { id: params.getValue("id"), status: "Connecting..." }
          dispatch(markConnecting(payload))
          initiateConnection(params.getValue("id"))
        }
        return (<><Chip label={params.getValue("connectionStatus")}></Chip>{(params.getValue("connectionStatus") === "connected" ? <IconButton size='small' onClick={() => triggerConnection()}><span className="iconify" data-icon="mdi:refresh-circle" data-inline="false"></span></IconButton> : params.getValue("connectionStatus") === "connecting..." ? "": <IconButton size='small' onClick={() => triggerConnection()}><span className="iconify" data-icon="mdi:arrow-right-circle" data-inline="false"></span></IconButton>)}</>)
      }
    },
    {
      field: "recordsIngested",
      headerName: "Ingested",
      flex: 0.15,
      renderCell: (params) => {
        const triggerIngestion = (params) => {
          const payload = { id: params.getValue("id"), status: "Ingestion in Progress..." }
          dispatch(markIngestionStatus(payload))
          actionIngestion(params.getValue("id"))
        }
        let cellTemp = ""
        if (params.getValue("ingested") && params.getValue("ingestionStatus"))
          cellTemp = (params.getValue("recordsIngested"))
        else if (!params.getValue("ingested") && params.getValue("ingestionStatus") === "InProgess")
          cellTemp = (<span>Ingestion in progress...</span>)
        else cellTemp = (<><Chip label="Not Ingested"></Chip><IconButton size='small' onClick={()=> {triggerIngestion(params)}}><span className="iconify" data-icon="mdi:arrow-right-circle" data-inline="false"></span></IconButton></>)
        return cellTemp
      }
    },
    {
      field: "empty",
      headerName: "Empty",
      flex: 0.1,
      renderCell: (params) => ((params.getValue("ingested") && params.getValue("ingestionStatus")) ? (params.getValue("recordsIngested")): (<></>))
    },
    {
      field: "bogus",
      headerName: "Bogus",
      flex: 0.1,
      renderCell: (params) => ((params.getValue("ingested") && params.getValue("ingestionStatus")) ? (params.getValue("recordsIngested")): (<></>))
    },
    {
      field: "cleansed",
      headerName: "Cleansed",
      flex: 0.1,
      renderCell: (params) => ((params.getValue("ingested") && params.getValue("ingestionStatus")) ? (params.getValue("recordsIngested")): (<></>))
    }

  ];

  const retrieveDataSources = (getState) => {
    dispatch(fetchDataSources());
  };
  const actionIngestion = (id) => {
    dispatch(triggerIngestion(id));
  };
  const initiateConnection = (id) => {
    console.log(id);
    dispatch(triggerConnectionCheck(id));
  };
  React.useEffect(() => {
    retrieveDataSources();
  }, []);

  return (
    <CTDataGrid
      data={props.dataSources}
      columns={columns}
      hasStarring={true}
      loading={props.dataSources.length ? false : true}
      onRemove={(params) => alert(params)}
      onBulkRemove={(params) => alert(JSON.stringify(params))}
      onDownload={(params) => alert(params)}
      onAddClick={(params) => alert("plus clicked")}
    ></CTDataGrid>
  )

};
const mapStateToProps = (state) => {
  return {
    dataSources: state.connections.dataSources || [],
  };
};
export default connect(mapStateToProps)(DataSources);
