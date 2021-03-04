import React from 'react';
import { Link } from "react-router-dom";
import { connect, useDispatch } from "react-redux";
import PageTitle from "../../components/PageTitle";
import { ReactComponent as TitleImage } from "../../assets/CustomerTitle.svg";

import CTDataGrid from "../../components/Table/CTDataGrid";
import CTChip from "../../components/Chip/CTChip";
import { fetchCustomerProfiles } from './store/action';

const FILTER_TYPES = {
    "Customer Value": { 
      selectMultiple: true,
      values: ["High", "Medium","Low"]
    },
}

const CustomersData = (props) => {
    const dispatch = useDispatch();
    const retrieveCustomerProfiles = () => {
        dispatch(fetchCustomerProfiles());
    };
    const columns = [
        {
          field: "customerProfile",
          headerName: " ",
          width: 50,
          renderCell: (params) => {
            const profile = params.getValue("customerProfile");
            return (
              <span style={{marginRight: "12px"}}>
              {
                profile === "M" ?
                    <span className="iconify" data-icon="mdi:face-man-profile" data-inline="false" />
                : profile === "F" ?
                    <span className="iconify" data-icon="mdi:face-woman-profile" data-inline="false" />
                : <></>
              }
              </span>
          )},
        },
        {
            field: "customerName",
            headerName: "Name",
            width: 300,
            renderCell: (params) => {
                const customerID = params.getValue("customerID");
                return (
                <Link to={`/customer-profiles/${customerID}`}>
                        {`${params.getValue("customerName")} `}
                </Link>
            )},
        },
        {
            field: "customerEmail",
            headerName: "Email",
            width: 200,
        },
        {
            field: "customerPhone",
            headerName: "Phone",
            width: 200,
        },
        {
            field: "accountNumber",
            headerName: "Account Number",
            width: 200,
        },
        {
            field: "customerValue",
            headerName: "Customer Value",
            width: 200,
            renderCell: (params) => {
                const customerValue = params.getValue("customerValue");
                return (
                <CTChip isNotMiddle={customerValue!=="Medium"} isWorking={customerValue==="High"} hasIcons={false}>
                       {customerValue}
                </CTChip>
            )},
        },
        {
            field: "customerEvents",
            headerName: "No. of Events",
            width: 200,
        }        
    ];
    React.useEffect(() => {
        retrieveCustomerProfiles();
    }, []);
    return (
    <>
        <PageTitle
            title="Customer Data"
            summaryText="Lorem ipsum dolor sit amet, consectetur"
            readMore="/"
            readMoreLabel="Learn More"
        >
            <TitleImage />
        </PageTitle>
        <CTDataGrid
            columns={columns}
            data={props.customerProfiles}
            isEditingEnabled={false}
            isSummaryEnabled
            summaryContent={[
                {value: "3.2",decimals:"1",suffix: "m",title: "Records"},
                {value: "600",title: "Data Sources"},
                {value: "34",title: "Stitched"},
                {value: "1.4",decimals:"1",suffix: "k",title: "Pinned"},
                {value: "4",title: "Avg. Strength"},
            ]}
            filterTypes={FILTER_TYPES}
            searchPlaceholder="Search Customers"
            isAddEnabled={false}
        />
    </>
)}
const mapStateToProps = (state) => ({
    customerProfiles: state.customerprofiles.customerProfiles || [],
});
export default connect(mapStateToProps)(CustomersData);