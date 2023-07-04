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

export const Size = {
  args: {
    size: '100px'
  },
};