import { Avatar } from './Avatar';

export default {
  title: 'Avatar',
  component: Avatar
};

export const Base = {
  args: {
  },
};

export const OnClickTest = {
  args: {
    onClick: () => console.log('click'),
  },
};