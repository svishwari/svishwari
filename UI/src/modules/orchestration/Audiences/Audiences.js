import React from 'react';
import { connect, useDispatch } from 'react-redux';
import CTDataGrid from '../../../components/Table/CTDataGrid';
import { fetchAudiences } from '../store/action';

const Audiences = (props) => {
  const dispatch = useDispatch();

  const columns = [
    { field: 'audience_name', headerName: 'Audience Name', flex: 0.3 },
    { field: 'updated', headerName: 'Last Updated', flex: 0.3 },
  ];

  React.useEffect(() => {
    dispatch(fetchAudiences());
  }, []);

  return (
    <CTDataGrid
      data={props.audiences}
      columns={columns}
      hasStarring
      loading={!props.audiences.length}
      pageName="Audiences"
      autoHeight
      isTopVisible={false}
      hideFooterPagination
    />
  );
};

const mapStateToProps = (state) => ({
    audiences: state.orchestration.audiences || [],
});

export default connect(mapStateToProps)(Audiences);
