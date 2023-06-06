import { MasterCard } from './MasterCard';

const data = {
    id: 1,
    academy_id: 1,
    title: 'Test Mastercard',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    teacher_bio_id: 1,
    composer_bio_id: 1,
    work_analysis_id: 1,
    partition_id: 1,
    instrument: 'piano',
    status: 'completed',
    created_at: '2021-05-05T14:00:00.000Z',
    created_by: '1',
    updated_by: '1',
};

export default {
  title: 'MasterCard',
  component: MasterCard,
  tags: ['autodocs'],
};

export const test = {
    args: {
        content: data,
    },
};