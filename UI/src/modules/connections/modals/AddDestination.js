import React from 'react';
import Select from "@material-ui/core/Select";
import CTModal from "../../../components/Modal/CTModal";
import CTLabel from "../../../components/Label/CTLabel";
import CTInput from "../../../components/Input/CTInput";
import "./AddDestination.scss";

const AddDestination = () => {
    const [selectedDestination, setselectedDestination] = React.useState(
        "Facebook"
      );
    const handleSelectedDestinationChange = (event) => {
        setselectedDestination(event.target.value);
    };
    const addDestinationContent = (<div className="ct-destination-modal">
          <CTLabel>Destination</CTLabel>
          <Select
            value={selectedDestination}
            onChange={(e) => handleSelectedDestinationChange(e)}
            label="Account ID"
            className="ct-destination-modal-select"
          >
            <option value="Facebook">Facebook</option>
          </Select>
          {selectedDestination === "Facebook" ? (
            <div className="ct-destination-fields">
              <span className="ct-destination-field-card">
                <CTLabel>IAM User Name</CTLabel>
                <CTInput placeholder="IAM User Name" />
              </span>
              <span className="ct-destination-field-card">
                <CTLabel>Password / Key</CTLabel>
                <CTInput placeholder="Password / Key" />
              </span>
            </div>
          ) : (
            ""
          )}
        </div>
    );
    return (
        <CTModal
            modalTitle="Add Destination"
            modalSubtitle="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
            modalBody={addDestinationContent}
            mainCTAText="Verify and Add"
        />
    )
}

export default AddDestination;
