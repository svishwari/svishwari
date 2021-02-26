import { Typography } from '@material-ui/core';
import React, { useState } from 'react';
// import { connect, useDispatch } from 'react-redux';
import { connect } from 'react-redux';
import CTModal from '../../../components/Modal/CTModal';
import CTSwitch from '../../../components/Switch/CTSwitch';
import FieldMapping from '../../../components/FieldMapping/FieldMapping';
import './DataIngest.scss';

const DataIngest = (modalProps) => {
  //   const dispatch = useDispatch();
  const [state, setState] = useState({
    Stitch: true,
    Cleanse: true,
    PLL: false,
  });
  const handleFlagChange = (event) => {
    setState({
      ...state,
      [event.target.name]: event.target.checked,
    });
  };
  const fieldsAvailable = ['City', 'County Codes', 'DOB', 'Email Address'];
  const ingestFlags = ["Stitch","Cleanse","PLL"];
  const IngestContent = (
    <div className="data-ingest-wrapper">
      <div className="ingest-flags">
        {
          ingestFlags.map(each=> 
            <div key={each} className="section">
              <Typography className="heading">
                {each}
              </Typography>
              <div>
                <CTSwitch
                  checked={state[each]}
                  onChange={handleFlagChange}
                  name={each}
                  label={state[each] ? 'Yes' : 'No'}
                />
              </div>
            </div>
          )
        }
      </div>
      <FieldMapping title="Field Mapping" fields={fieldsAvailable} />
    </div>
  );
  return (
    <CTModal
      modalTitle="Ingest Data Source"
      modalSubtitle={`Ingest data source for "${modalProps.fileName}"`}
      modalBody={IngestContent}
      mainCTAText="Ingest"
      disableBackdropClick
      disableEscapeKeyDown
    />
  );
};

const mapStateToProps = (state) => ({
  modal: state.modal || [],
});
export default connect(mapStateToProps)(DataIngest);
