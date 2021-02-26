import React from 'react';
import CTModal from "../../../components/Modal/CTModal";
import CTLabel from "../../../components/Label/CTLabel";
import CTInput from "../../../components/Input/CTInput";
import CTSelect from "../../../components/Select/CTSelect";
import "./AddDataSource.scss";

const REQUIRED_FIELDS = {
  "Amazon S3": [
    {
      label: "IAM User Name",
      placeholder: "IAM User Name",
    },
    {
      label: "Password / Key",
      placeholder: "**********",
      type: "password",
    },
    {
      label: "Filename",
      placeholder: "Unique name for your file",
    },
    {
      label: "Filepath",
      placeholder: "example.csv",
    },
  ],
  "CDP": [
    {
      label: "IAM User Name",
      placeholder: "IAM User Name",
    },
    {
      label: "Password / Key",
      placeholder: "**********",
      type: "password",
    },
  ]
};

const DATA_SOURCES = Object.keys(REQUIRED_FIELDS);

const AddDataSource = () => {
    const [selectedDataSource, setselectedDataSource] = React.useState(DATA_SOURCES[0]);
    const handleSelectedDataSourceChange = (event) => {
        setselectedDataSource(event.target.value);
    };
    const addDataSourceContent = (
        <div className="ct-datasource-modal">
          <CTLabel>Data Source</CTLabel>
          <CTSelect selectOptions={DATA_SOURCES} onChange={handleSelectedDataSourceChange}/>
          <div className="ct-datasource-fields">
            { 
              REQUIRED_FIELDS[selectedDataSource].map(each=>(
                <span key={each.label} className="ct-datasource-field-card">
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
            modalTitle="Add Data Source"
            modalSubtitle="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
            modalBody={addDataSourceContent}
            mainCTAText="Verify and Add"
        />
    )
}

export default AddDataSource;
