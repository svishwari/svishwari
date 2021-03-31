import React from 'react';
import { connect, useDispatch } from "react-redux";
import { Link, useParams } from "react-router-dom";

import './CustomerData.scss';

import { Box, Button } from '@material-ui/core';
import SummaryCard from "../../components/Cards/SummaryCard/SummaryCard";
import CTChip from "../../components/Chip/CTChip";
import CTList from "../../components/List/List";
import CTPopover from "../../components/Popover/CTPopover";
import CTFilter from "../../components/Filter/CTFilter";

import { fetchCustomerProfile } from './store/action';

const summaryContent= [
    {value: "1 Year 2 Months",title: "Customer Length"},
    {value: (<CTChip hasIcons={false} isWorking>High</CTChip>),title: "Strength"},
    {value: "2/12/2021",title: "Last Event"},
    {value: "$60.23",title: "Value"},
    {value: "1.2 Months",title: "Conversion Time"},
];

const EVENTS_COLUMN = [
    {
      field: "eventType",
      headerName: "Event Type",
      flex: 0.6,
    },
    {
        field: "charge",
        headerName: "Charge (USD)",
        flex: 0.2,
    },
    {
        field: "date",
        headerName: "Date",
        flex: 0.2,
    }     
];

const INCLUDED_COLUMN = [
    {
        field: "orchestrationName",
        headerName: "Orchestration Name",
        flex: 0.4,
    },
    {
        field: "connectionStatus",
        headerName: "Status",
        flex: 0.3,
        renderCell: (params) => (
            <>
                {params.getValue("connectionStatus") !== "Connecting..." ? (
                    <CTChip
                    hasIcons
                    isWorking={params.getValue("connectionStatus") === "Connected"}
                    >
                    {params.getValue("connectionStatus")}
                    </CTChip>
                ) : (
                    <span>Connecting...</span>
                )}
            </>
        ),
    },
    {
        field: "openIn",
        headerName: "Open In",
        flex: 0.2,
        renderCell: () => (
            <CTPopover
              popoverContent={
                <Box display="flex" flexDirection="column">
                  <Button><span className="iconify" data-icon="logos:facebook" data-inline="false" />{'\u00A0'}Facebook</Button>
                  <Button><span className="iconify" data-icon="logos:google-analytics" data-inline="false" />{'\u00A0'}Google</Button>
                </Box>
              }
            >
              <Button color="primary" style={{ textTransform: 'capitalize' }}>
                Open in <span className="iconify" data-icon="zmdi-caret-down" data-inline="false" />
              </Button>
            </CTPopover>
        ),
    },
];

const DATA_SOURCE_COLUMN = [
    {
        field: "fileName",
        headerName: "File Name",
        flex: 0.2,
        renderCell: (params) => (
            <Link to={() => false}>
            {params.getValue("fileName")}{" "}
            <span
                className="iconify"
                data-icon="mdi:open-in-new"
                data-inline="false"
            />
            </Link>
        ),
    },
    {
        field: "source",
        headerName: "Source",
        flex: 0.2,
    },
    {
        field: "lastUpdated",
        headerName: "Last Updated",
        flex: 0.2,
    },
    {
        field: "stitched",
        headerName: "Stitched",
        flex: 0.2,
    },
    {
        field: "pinned",
        headerName: "Pinned",
        flex: 0.2,
    },
];

const FILTER_TYPES = {
    "Event Type": {
      selectMultiple: true,
      values: ["Purchase", "Subscription Purchase"]
    },
    "Charge": { 
      selectMultiple: true,
      values: ["10.23"]
    },
}

const CustomerData = (props) => {
    const {profileID} = useParams();
    const dispatch = useDispatch();
    const userProfilePhoto = props.customerProfile.customerProfile;
    const userName = props.customerProfile.customerName;
    const accountID = props.customerProfile.accountNumber;

    const USER_PII_DATA = [
        {Email: "example@gmail.com"},
        {Age: "21"},
        {Gender:"Female"},
        {Phone: "555-555-5555"},
        {City: "Akron"},
        {State: "Ohio"},
    ]
    const retrieveCustomerProfile = () => {
        dispatch(fetchCustomerProfile(profileID));
    };
    React.useEffect(() => {
        retrieveCustomerProfile();
    }, []);
    return (
        <div className="customer-data-wrapper">
            <div className="cd-top-header">
                <Link className='cd-view-all' to='/customer-profiles'>&lt; View All Customers</Link>
                <button type="button" className="cd-download-btn">
                    <span
                    className="iconify"
                    data-icon="mdi:download"
                    data-inline="false"
                    />
                </button>
            </div>
            <div className="cd-content">
                <div className="cd-content-account-details">
                    <div className="cd-profile-image">
                        {
                            userProfilePhoto === "M" ?
                                <span className="iconify" data-icon="mdi:face-man-profile" data-inline="false" />
                            : userProfilePhoto === "F" ?
                                <span className="iconify" data-icon="mdi:face-woman-profile" data-inline="false" />
                            : <></>
                        }
                        <span className="cd-customer-name"> {userName}</span>
                    </div>
                    <div className="cd-customer-acc-id">
                        <span className="cd-customer-acc-id-label">Account ID </span> 
                        {accountID}
                    </div>
                </div>
                <div className="cd-cards">
                    {summaryContent.map(content=>
                        <SummaryCard hasAnimation={false} key={content.title} width="185px" value={content.value} suffix={content.suffix} title={content.title}/>
                    )}
                </div>
                <div className="cd-customer-insights">
                    <div className="cd-customer-title">Customer Insights</div>
                    <div className="cd-insights-card">
                        <div className="col-3 pl-0">
                            {
                                USER_PII_DATA.map(each => 
                                    <div key={each[Object.keys(each)[0] ]} className="cd-customer-detail-container">
                                        <span className="cd-customer-detail-label">{Object.keys(each)[0]}</span>
                                        <span className="cd-customer-detail">{each[Object.keys(each)[0] ]}</span>
                                    </div>
                                )
                            }                          
                        </div>
                        <div className="col-7">
                            <div>Do something here!</div>
                        </div>
                    </div>
                </div>
                <div className="cd-customer-events">
                    <div className="cd-customer-event-title">
                        <div className="cd-customer-title">
                            Events
                        </div>
                        <div className="cd-customer-filter">
                            <CTFilter filterTypes={FILTER_TYPES}/>
                        </div>
                    </div>
                    <CTList
                        columns={EVENTS_COLUMN}
                        rows={props.customerProfile.events || []}
                    />
                </div>
                <div className="cd-customer-included">
                    <div className="cd-customer-title">Included Segments &amp; Audiences</div>
                    <CTList
                        columns={INCLUDED_COLUMN}
                        rows={props.customerProfile.includedIn || []}
                        headerHeight={0}
                    />
                </div>
                <div className="cd-customer-datasource">
                    <div className="cd-customer-title">{`Data Sources (${props.customerProfile.dataSources ? props.customerProfile.dataSources.length : "0"})`}</div>
                    <CTList
                        columns={DATA_SOURCE_COLUMN}
                        rows={props.customerProfile.dataSources || []}
                    />
                </div>
            </div>
        </div>
    )
}
const mapStateToProps = (state) => ({
    customerProfile: state.customerprofiles.customerProfile || [],
});
export default connect(mapStateToProps)(CustomerData);
