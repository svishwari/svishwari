import React from 'react';
import { Link, useParams } from "react-router-dom";
import { connect, useDispatch } from "react-redux";
import { Box, Button } from '@material-ui/core';

import SummaryCard from "../../../components/Cards/SummaryCard/SummaryCard";
import CTList from "../../../components/List/List";
import CTFilter from "../../../components/Filter/CTFilter";
import CTSecondaryButton from '../../../components/Button/CTSecondaryButton';
import CTPrimaryButton from '../../../components/Button/CTPrimaryButton';
import CTUSAMap from '../../../components/Charts/CTUSAMap';
import CTChip from '../../../components/Chip/CTChip';
import CTPopover from "../../../components/Popover/CTPopover";

import "./SegmentSummary.scss";
import { fetchSegmentSummary } from "../store/action";

const summaryContent=[
    {value: 3.6,suffix: "M",decimal:1,title: "Segment Size"},
    {value: 1.3,suffix: "K",decimal:1,title: "Site Vitits"},
    {value: 0.124,suffix: "%",decimal:3,title: "Site Visit Rate"},
    {value: 600,title: "Converstions"},
    {value: 0.234,suffix: "%",decimal:3,title: "Site Visiting Rate"},
    {value: 12,suffix: "x",title: "Conversion Propensity"},
];

const CUSTOMERS_COLUMN = [
    {
      field: "customerName",
      headerName: "Customer Name",
      width: 250,
    },
    {
        field: "results",
        headerName: "Results",
        width: 150,
    },
    {
        field: "device",
        headerName: "Device",
        width: 150,
    },
    {
        field: "age",
        headerName: "Age",
        width: 150,
    },   
    {
        field: "gender",
        headerName: "Gender",
        width: 150,
    },
    {
        field: "incomeRange",
        headerName: "Income Range",
        width: 250,
    }, 
];

const DESTINATION_COLUMN = [
    {
      field: "destination",
      headerName: " ",
      width: 50,
      renderCell: (params) => {
        const destinationLogo = params.getValue("destination")
        return (
        <>
          <span style={{marginRight: "12px"}}>
          {
            destinationLogo === "fb" ?
              <span className="iconify" data-icon="logos:facebook" data-inline="false" />
            : destinationLogo === "sfmc" ?
              <span className="iconify" data-icon="logos:salesforce" data-inline="false" />
            : destinationLogo === "ga" ?
              <span className="iconify" data-icon="grommet-icons:google" data-inline="false" />
            : <></>
          }
          </span>
        </>
      )},
    },
    {
      field: "destinationName",
      headerName: "Destination",
      flex: 0.2,
      renderCell: (params) => (
        <>
          <Link to="/destinations">
            {`${params.getValue("destinationName")} `}
            <span
              className="iconify"
              data-icon="mdi:open-in-new"
              data-inline="false"
            />
          </Link>
        </>
      ),
    },
    {
      field: "account",
      headerName: "Account Name",
      flex: 0.1,
    },
    {
      field: "lastUpdated",
      headerName: "Last Updated",
      flex: 0.15,
    },
    {
      field: "status",
      headerName: "Status",
      flex: 0.15,
      renderCell: (params) => (
          <>
            {params.getValue("status") !== "Connecting..." ? (
              <CTChip
                hasIcons
                isWorking={params.getValue("status") === "Connected"}
              >
                {params.getValue("status")}
              </CTChip>
            ) : (
              <span>Connecting...</span>
            )}
          </>
        ),
    },
    
];

const FILTER_TYPES = {
    "Device": {
      selectMultiple: true,
      values: ["Mobile", "Desktop"]
    },
    "Age": { 
      selectMultiple: true,
      values: ["<18","18-25","25-50",">50"]
    },
    "Gender": { 
        selectMultiple: true,
        values: ["Male","Female","Other"]
    },
    "Result": { 
        selectMultiple: true,
        values: ["High","Medium","Low"]
    },
}


const states= [{ WA: 90 }, { NY: 90 }, { MT: 90 }, { NY: 28 }, { CA: 18 }, { TX: 90 }];
const stateList= [
    {
      id: 1,
      name: 'Washington',
      value: '50%',
    },
    {
      id: 2,
      name: 'New York',
      value: '48%',
    },
    {
      id: 3,
      name: 'Montana',
      value: '48%',
    },
    {
      id: 4,
      name: 'New York',
      value: '48%',
    },
    {
      id: 5,
      name: 'California',
      value: '48%',
    },
    {
      id: 6,
      name: 'Texas',
      value: '48%',
    },
    {
        id: 7,
        name: 'Texas',
        value: '48%',
    },
];

const SegmentSummary = (props) => {
    const dispatch = useDispatch();

    const {segmentID} = useParams();
    const { segmentName, created, models } = props.segmentSummary;

    const retrieveSegment = () => {
        dispatch(fetchSegmentSummary(segmentID));
    };
    const insightCard = () => (
        <div className="insight-wrap">
            <div className="worldmap">
              <CTUSAMap data={states} />
            </div>
            <div className="table">
              <CTList
                columns={[
                  {
                    field: 'name',
                    headerName: 'Name',
                    flex: 0.7,
                  },
                  {
                    field: 'value',
                    headerName: 'Value',
                    flex: 0.3,
                  },
                ]}
                rows={stateList}
              />
            </div>
        </div>
    );
    React.useEffect(() => {
        retrieveSegment();
    }, []);
    return (
        <div className="customer-data-wrapper">
            <div className="cd-top-header">
                <Link className='cd-view-all' to='/orchestration/segments'>&lt; View All Segments</Link>
                <div className="cd-top-right">
                    <CTSecondaryButton customClass="ml-2 mr-2" btnWidth="auto">Deliver</CTSecondaryButton>
                    <CTPopover
                        popoverContent={
                            <Box display="flex" flexDirection="column">
                            <Button><span className="iconify" data-icon="logos:facebook" data-inline="false" />{'\u00A0'}Facebook</Button>
                            <Button><span className="iconify" data-icon="logos:google-analytics" data-inline="false" />{'\u00A0'}Google</Button>
                            </Box>
                        }
                        >
                        <CTSecondaryButton customClass="ml-2 mr-2" btnWidth="auto">
                            Open In
                        </CTSecondaryButton>
                    </CTPopover>
                    <CTPopover
                        popoverContent={
                            <Box display="flex" flexDirection="column">
                                <div>DOWNLOAD</div>
                                <div>.CSV</div>
                                <div>.JSON</div>
                                <div>.PDF</div>
                            </Box>
                        }
                        >
                        <CTSecondaryButton customClass="ml-2 mr-2 cd-download-btn" btnWidth="auto">
                            <span
                                className="iconify"
                                data-icon="mdi:download"
                                data-inline="false"
                            />
                        </CTSecondaryButton>
                    </CTPopover>
                    <CTPrimaryButton>Configure</CTPrimaryButton>
                </div>
            </div>
            <div className="cd-content">
                <div className="cd-content-account-details">
                    <div className="cd-profile-image">
                        <span className="cd-customer-name"> {segmentName}</span>
                    </div>
                    <div className="cd-customer-acc-id">
                        <span className="cd-customer-acc-id-label">Time Created </span> 
                        <span className="cd-customer-acc-id">{created}</span>
                        <span className="cd-customer-acc-id-label">Models(s) </span> 
                        <span className="cd-customer-acc-id">{models && models[0]}</span>
                        <span className="cd-customer-acc-id-label">File Source </span> 
                        <span className="cd-customer-acc-id">
                            <Link to={() => false}>
                                MyAmazing
                                <span
                                    className="iconify"
                                    data-icon="mdi:open-in-new"
                                    data-inline="false"
                                />
                            </Link>
                        </span>
                    </div>
                </div>
                <div className="cd-cards">
                    {summaryContent.map(content=>
                        <SummaryCard decimals={content.decimal} key={content.title} width="185px" value={content.value} suffix={content.suffix} title={content.title}/>
                    )}
                </div>
                <div className="cd-customer-insights">
                {insightCard({
                    name: 'Insight',
                })}
                </div>
                <div className="cd-customer-events">
                    <div className="cd-customer-event-title">
                        <div className="cd-customer-title">
                            Customers
                        </div>
                        <div className="cd-customer-filter">
                            <CTFilter filterTypes={FILTER_TYPES}/>
                        </div>
                    </div>
                    <CTList
                        headerHeight={28}
                        columns={CUSTOMERS_COLUMN}
                        rows={props.segmentSummary.customers || []}
                    />
                </div>
                <div className="cd-customer-datasource">
                    <div className="cd-customer-title">Destinations</div>
                    <CTList
                        headerHeight={28}
                        columns={DESTINATION_COLUMN}
                        rows={props.segmentSummary.destinations || []}
                    />
                </div>
            </div>
        </div>
    )
}
const mapStateToProps = (state) => ({
    segmentSummary: state.orchestration.segmentSummary || [],
});
export default connect(mapStateToProps)(SegmentSummary);