import React from 'react';
import { connect } from 'react-redux';

import AddDataSource from '../connections/modals/AddDataSource';
import AddDestination from '../connections/modals/AddDestination';
import AddSegment from '../orchestration/modals/AddSegment';
import DataIngest from '../connections/modals/DataIngest';
import FetchScore from '../orchestration/modals/FetchScore';


const MODAL_COMPONENTS = {
  'OPEN_ADD_DATA_SOURCE': AddDataSource,
  'OPEN_ADD_DESTINATION': AddDestination,
  'OPEN_ADD_SEGMENT': AddSegment,
  'TRIGGER_INGEST': DataIngest,
  'SHOW_FETCH_SCORE': FetchScore,
}

const ModalRoot = (props) => {
  if (!props.modal.modalType) {
    return <></>;
  }
  const SpecificModal = MODAL_COMPONENTS[props.modal.modalType];
  return <SpecificModal {...props.modal.modalProps} />;
};

const mapStateToProps = (state) => ({
  modal: state.modal || [],
});
export default connect(mapStateToProps)(ModalRoot);
