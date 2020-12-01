if __name__ == "__main__":
    import torch
    from trainer.train_utils import generate_lyrics

    # 모델 불러오기
    pretrained_model = "../data/model/"
    model = torch.load(pretrained_model)

    # 평가 모드로 전환
    model.eval()
    model.batch_size = 1

    # 가사 생성하기
    lyrics = generate_lyrics(["사랑"])
    print(lyrics)