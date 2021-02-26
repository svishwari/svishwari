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
    const fieldsAvailable = ['City', 'County Codes', 'DOB', 'Email Address']
  const IngestContent = (
    <div className="data-ingest-wrapper">
      <div className="ingest-flags">
        <div className="section">
          <Typography className="heading">
            Stitch
          </Typography>
          <div>
            <CTSwitch
              checked={state.Stitch}
              onChange={handleFlagChange}
              name="Stitch"
              label={state.Stitch ? 'Yes' : 'No'}
            />
          </div>
        </div>
        <div className="section">
          <Typography className="heading">
            Cleanse
          </Typography>
          <div>
            <CTSwitch
              checked={state.Cleanse}
              onChange={handleFlagChange}
              name="Cleanse"
              label={state.Cleanse ? 'Yes' : 'No'}
            />
          </div>
        </div>
        <div className="section">
          <Typography className="heading">
            PLL
          </Typography>
          <div>
            <CTSwitch
              checked={state.PLL}
              onChange={handleFlagChange}
              name="PLL"
              label={state.PLL ? 'Yes' : 'No'}
            />
          </div>
        </div>
      </div>
      <div className="field-mapping-wrapper">
        <FieldMapping title="Field Mapping" fields={fieldsAvailable} />
      </div>
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
