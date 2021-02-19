import { Chip, IconButton } from "@material-ui/core";
import React from "react";
import { connect, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import CTDataGrid from "../../../components/Table/CTDataGrid";
import { fetchDataSources, triggerIngestion, triggerConnectionCheck,addNewDataSource } from "../store/action";
import CTModal from "../../../components/Modal/CTModal";
import CTLabel from "../../../components/Label/CTLabel";
import CTInput from "../../../components/Input/CTInput";
import Select from '@material-ui/core/Select';
import './DataSource.scss';
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
  const [selectedDataSource, setselectedDataSource] = React.useState('Amazon S3');
  const handleSelectedDataSourceChange = (event) => {
    setselectedDataSource(event.target.value);
  };
  const addDataSourceContent = (
    <div className='ct-datasource-modal'>
      <CTLabel>Data Source</CTLabel>
      <Select
          value={selectedDataSource}
          onChange={(e)=>handleSelectedDataSourceChange(e)}
          label="Account ID"
        >
          <option  value={'Amazon S3'}>Amazon S3</option>
          <option value={'CDP'}>CDP</option>
          <option value={'Facebook'}>Facebook</option>
      </Select>
      <CTLabel>Account ID</CTLabel>
      <CTInput placeholder={'Account ID'}></CTInput>
      { selectedDataSource==='Amazon S3' ?
        <div>
        <CTLabel>IAM User Name</CTLabel>
        <CTInput placeholder={'IAM User Name'}></CTInput>
        <CTLabel>Password / Key</CTLabel>
        <CTInput placeholder={'Password / Key'}></CTInput>
        <CTLabel>Filename</CTLabel>
        <CTInput placeholder={'Unique name for your file'}></CTInput>
        <CTLabel>Filepath</CTLabel>
        <CTInput placeholder={'example.csv'}></CTInput>
        </div>
      : ''
      }
      { selectedDataSource==='Facebook' ?
        <div>
        <CTLabel>IAM User Name</CTLabel>
        <CTInput placeholder={'IAM User Name'}></CTInput>
        <CTLabel>Password / Key</CTLabel>
        <CTInput placeholder={'Password / Key'}></CTInput>
        <CTLabel>Filename</CTLabel>
        <CTInput placeholder={'Unique name for your file'}></CTInput>
        </div>
      : ''
      }
      { selectedDataSource==='CDP' ?
        <div>
        <CTLabel>IAM User Name</CTLabel>
        <CTInput placeholder={'IAM User Name'}></CTInput>
        <CTLabel>Password / Key</CTLabel>
        <CTInput placeholder={'Password / Key'}></CTInput>
        </div>
      : ''
      }
    </div>
  );
  const childRef = React.useRef();

  return (
    <>
    <CTDataGrid
      data={props.dataSources}
      columns={columns}
      hasStarring={true}
      loading={props.dataSources.length ? false : true}
      onRemove={(params) => alert(params)}
      onBulkRemove={(params) => alert(JSON.stringify(params))}
      onDownload={(params) => alert(params)}
      onAddClick={() => { childRef.current.handleOpen() }}
      pageName={"Data Source"}
    ></CTDataGrid>
    <CTModal 
      ref={childRef}
      modalTitle="Add Data Source"
      modalSubtitle="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
      modalBody={addDataSourceContent}
      mainCTAText="Verify and Add"
      onComplete={()=> dispatch(addNewDataSource())}
    />
    </>
  )
};
const mapStateToProps = (state) => {
  return {
    dataSources: state.connections.dataSources || [],
  };
};
export default connect(mapStateToProps)(DataSources);
