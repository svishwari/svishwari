import React from 'react';
import { useDispatch } from 'react-redux';
import CTModal from "../../../components/Modal/CTModal";
import CTLabel from "../../../components/Label/CTLabel";
import CTInput from "../../../components/Input/CTInput";
import CTSelect from "../../../components/Select/CTSelect";
import "./AddDestination.scss";
import {
  addNewDestination
} from "../store/action";

const REQUIRED_FIELDS = {
  "Facebook": [
    {
      label: "Ad Account ID",
      placeholder: "*********************",
      type: "password",
    },
    {
      label: "Access Token",
      placeholder: "**********",
      type: "password",
    },
    {
      label: "App ID",
      placeholder: "**********",
      type: "password",
    },
    {
      label: "App Secret",
      placeholder: "**********",
      type: "password",
    },
  ],
  "Google Analytics": [
    {
      label: "Ad Account ID",
      placeholder: "*********************",
      type: "password",
    },
    {
      label: "Access Token",
      placeholder: "**********",
      type: "password",
    },
    {
      label: "App ID",
      placeholder: "**********",
      type: "password",
    },
  ],
  "Sales Force Marketing Cloud": [
    {
      label: "Ad Account ID",
      placeholder: "*********************",
      type: "password",
    },
    {
      label: "Access Token",
      placeholder: "**********",
      type: "password",
    },
    {
      label: "App ID",
      placeholder: "**********",
      type: "password",
    },
  ],
};

const DESTINATION = Object.keys(REQUIRED_FIELDS);

const AddDestination = () => {
    const [selectedDestination, setselectedDestination] = React.useState(DESTINATION[0]);
    const handleSelectedDestinationChange = (event) => {
        setselectedDestination(event.target.value);
    };
    const dispatch = useDispatch();
    const addDestinationContent = (
        <div className="ct-destination-modal">
          <CTLabel>Select Destination</CTLabel>
          <CTSelect selectOptions={DESTINATION} onChange={handleSelectedDestinationChange}/>
          <div className="account-name-container">
            <CTLabel>Account Name</CTLabel>
            <CTInput placeholder="Account Name" />
          </div>
          <div className="ct-destination-fields">
            { 
              REQUIRED_FIELDS[selectedDestination].map(each=>(
                <span key={each.label} className="ct-destination-field-card">
                  <CTLabel>{each.label}</CTLabel>
                  <CTInput placeholder={each.placeholder} type={each.type} />
                </span>
              ))
            }
          </div>
        </div>
    );
    return (
        <CTModal
            modalTitle="Add Destination"
            modalSubtitle={`Connect a destination so that you can get a deeper insight into your 
            customers, segments, and audiences.`}
            modalBody={addDestinationContent}
            mainCTAText="Verify and Add"
            onComplete={()=> dispatch(addNewDestination())}
        />
    )
}

export default AddDestination;
