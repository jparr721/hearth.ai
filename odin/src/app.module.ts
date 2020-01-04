import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

import ormconfig from './db/config';

@Module({
  imports: [TypeOrmModule.forRoot(ormconfig)],
})
export class AppModule {}
