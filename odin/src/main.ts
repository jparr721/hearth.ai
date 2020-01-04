import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import * as dotenv from 'dotenv';
import get from 'lodash/get';

import { AppModule } from './app.module';

dotenv.config();

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe({ whitelist: true }));

  const options = new DocumentBuilder()
    .setTitle('Odin')
    .setDescription('Odin API service')
    .setVersion('1.0')
    .addTag('odin')
    .build();

  const document = SwaggerModule.createDocument(app, options);
  SwaggerModule.setup('_docs', app, document);

  const port = Number(get(process.env.APP_PORT, 3000));

  await app.listen(port);
}

bootstrap();
