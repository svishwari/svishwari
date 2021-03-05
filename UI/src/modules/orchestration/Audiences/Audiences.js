import React from 'react';
import { connect, useDispatch } from 'react-redux';
import { Typography } from '@material-ui/core';
import CTDataGrid from '../../../components/Table/CTDataGrid';
import { fetchAudiences } from './store/action';

const Audiences = (props) => {
  const dispatch = useDispatch();

  const getAudiences = () => {
    if (props.audiences.audiences.length > 0) {
      return props.audiences.audiences;
    }
    return [];
  };

  const columns = [
    { field: 'name', headerName: 'Name' },
  ];

  React.useEffect(() => {
    dispatch(fetchAudiences());
  }, []);
  return (
    <div className="dashboard-wrapper">
      <div className="content-wrapper">
        <Typography variant="h5" className="recent-heading">
          Audiences
        </Typography>
        <CTDataGrid
          autoHeight
          hasStarring={false}
          isTopVisible={false}
          hideFooterPagination
          showTopBar={false}
          headerHeight={0}
          editing={false}
          columns={columns}
          data={getAudiences()}
        />
      </div>
    </div>
  );
};

const mapStateToProps = (state) => ({
  userInfo: state.user.loggedInUser || [],
  audiences: state.audiences,
});

export default connect(mapStateToProps)(Audiences);
