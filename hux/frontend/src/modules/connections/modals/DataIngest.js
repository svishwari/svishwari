import { Typography } from '@material-ui/core';
import React, { useState } from 'react';
import { connect, useDispatch } from 'react-redux';
import CTModal from '../../../components/Modal/CTModal';
import CTSwitch from '../../../components/Switch/CTSwitch';
import FieldMapping from '../../../components/FieldMapping/FieldMapping';
import './DataIngest.scss';
import {
  triggerIngestion,
} from "../store/action";


const markIngestionStatus = (payload) => ({
  type: "updateInestionStatus",
  payload,
});

const DataIngest = (modalProps) => {
  const dispatch = useDispatch();
  const [state, setState] = useState({
    Stitch: true,
    Cleanse: true,
    PII: false,
  });
  const startIngestion = () => {
    dispatch(markIngestionStatus(modalProps))
    actionIngestion(modalProps.id);
  };
  const actionIngestion = (id) => {
    dispatch(triggerIngestion(id));
  };
  const handleFlagChange = (event) => {
    setState({
      ...state,
      [event.target.name]: event.target.checked,
    });
  };
  const fieldsAvailable = ['City', 'County Codes', 'DOB', 'Email Address'];
  const ingestFlags = ["Stitch","Cleanse","PII"];
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
      onComplete={startIngestion}
    />
  );
};

const mapStateToProps = (state) => ({
  modal: state.modal || [],
});
export default connect(mapStateToProps)(DataIngest);
