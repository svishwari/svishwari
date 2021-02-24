import React from 'react';
import Select from "@material-ui/core/Select";
import CTModal from "../../../components/Modal/CTModal";
import CTLabel from "../../../components/Label/CTLabel";
import CTInput from "../../../components/Input/CTInput";
import "./AddDataSource.scss";

const AddDataSource = () => {
    const [selectedDataSource, setselectedDataSource] = React.useState(
        "Amazon S3"
      );
    const handleSelectedDataSourceChange = (event) => {
        setselectedDataSource(event.target.value);
    };
    const addDataSourceContent = (<div className="ct-datasource-modal">
          <CTLabel>Data Source</CTLabel>
          <Select
            value={selectedDataSource}
            onChange={(e) => handleSelectedDataSourceChange(e)}
            label="Account ID"
            className="ct-datasource-modal-select"
          >
            <option value="Amazon S3">Amazon S3</option>
            <option value="CDP">CDP</option>
            <option value="Facebook">Facebook</option>
          </Select>
    
          {selectedDataSource === "Amazon S3" ? (
            <div className="ct-datasource-fields">
              <span className="ct-datasource-field-card">
                <CTLabel>IAM User Name</CTLabel>
                <CTInput placeholder="IAM User Name" />
              </span>
              <span className="ct-datasource-field-card">
                <CTLabel>Password / Key</CTLabel>
                <CTInput placeholder="Password / Key" />
              </span>
              <span className="ct-datasource-field-card">
                <CTLabel>Filename</CTLabel>
                <CTInput placeholder="Unique name for your file" />
              </span>
              <span className="ct-datasource-field-card">
                <CTLabel>Filepath</CTLabel>
                <CTInput placeholder="example.csv" />
              </span>
            </div>
          ) : (
            ""
          )}
          {selectedDataSource === "CDP" ? (
            <div className="ct-datasource-fields">
              <span className="ct-datasource-field-card">
                <CTLabel>IAM User Name</CTLabel>
                <CTInput placeholder="IAM User Name" />
              </span>
              <span className="ct-datasource-field-card">
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
            modalTitle="Add Data Source"
            modalSubtitle="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
            modalBody={addDataSourceContent}
            mainCTAText="Verify and Add"
        />
    )
}

export default AddDataSource;
