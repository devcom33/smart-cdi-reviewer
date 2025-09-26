package org.heymouad.backend.services.servicesImpl;

import lombok.RequiredArgsConstructor;
import org.heymouad.backend.dtos.ContractMessage;
import org.heymouad.backend.dtos.ContractResponse;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;

import java.util.UUID;


@Service
@RequiredArgsConstructor
public class ContractReviewProducer {
    private final RabbitTemplate rabbitTemplate;

    public String sendToQueue(ContractResponse contract){
        String id = UUID.randomUUID().toString();
        ContractMessage message = new ContractMessage(
                id,
                contract.filename(),
                contract.extractedText(),
                contract.header()
        );
        rabbitTemplate.convertAndSend("contract-exchange", "contract-routing-key", message);

        return id;
    }
}
