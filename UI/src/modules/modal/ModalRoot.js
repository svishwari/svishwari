import React from 'react';
import { connect } from 'react-redux';

import AddDataSource from '../connections/modals/AddDataSource';
import AddDestination from '../connections/modals/AddDestination';
import DataIngest from '../connections/modals/DataIngest';

const MODAL_COMPONENTS = {
  OPEN_ADD_DATA_SOURCE: AddDataSource,
  OPEN_ADD_DESTINATION: AddDestination,
  TRIGGER_INGEST: DataIngest,
};

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
