import { ConnectionOptions } from 'typeorm';
import get from 'lodash/get';

const config: ConnectionOptions = {
  type: 'postgres',

  host: get(process.env.DB_HOST, 'localhost'),
  port: Number(get(process.env.DB_PORT, 5432)),
  username: get(process.env.DB_USER, 'odin'),
  password: get(process.env.DB_PASS, 'odin'),
  database: get(
    process.env.DB_NAME,
    `odin_${get(process.env.APP_ENV, 'development')}`,
  ),

  entities: [__dirname + '/../**/*.entity{.ts,.js}'],

  synchronize: false,

  migrationsRun: true,

  logging: 'all',

  migrations: [__dirname + '/migrations/**/*{.ts,.js}'],
  cli: {
    migrationsDir: 'src/db/migrations',
  },
};

export = config;
