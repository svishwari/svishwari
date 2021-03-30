import { React } from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';

const styles = {
  heading: {
    color: '#3E4246',
    fontSize: 12,
    fontWeight: 600,
    textTransform: 'none'
  },
  listItem: {
    color: '#3E4246',
    fontSize: 14,
    fontWeight: 600,
    padding: 10
  }
}

export default function CTNewList(props) {
  return (
    <>

      <List {...props}>
        {props.showHeading && <ListItem style={styles.heading}>{props.heading}</ListItem>}
        <Divider />
        {props.items.map(item =>
          <>
            <ListItem style={styles.listItem} key={item.id}>{item.title}</ListItem>
            <Divider />
          </>
        )}
      </List>
    </>
  );
}
