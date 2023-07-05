import { Field } from './Field';

export default {
  title: 'Field',
  component: Field,
  tags: ['autodocs'],
};

export const Default = {
    args: {
        placeholder: 'Test Field',
        type: 'text',
    },
};

export const Search = {
    args: {
        placeholder: 'Test Field',
        type: 'search',
    },
};

export const Password = {
    args: {
        placeholder: 'Enter your password',
        type: 'password',
    },
};